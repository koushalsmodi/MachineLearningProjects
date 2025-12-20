"""
This project is a LangGraph-based RAG agent that:

1. Loads a PDF

2. Splits it into chunks

3. Creates embeddings

4. Stores them in ChromaDB

5. Exposes a retriever as a tool

6. Uses an LLM that can call tools

7. Orchestrates everything with a LangGraph state machine

8. Loops until no more tool calls are needed

9. Returns a final grounded answer to the user
"""

from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, SystemMessage, ToolMessage, HumanMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI # Reads user questions, decides whether to answer directly , or decides to call your retriever tool
from langchain_openai import OpenAIEmbeddings # A wrapper that converts text to vectors (numerical embeddings) # Without embeddings - no semantic search.
from langchain_community.document_loaders import PyPDFLoader # Reads PDFs, extracts text page by page, wraps each page as a LangChain Document
from langchain_text_splitters import RecursiveCharacterTextSplitter # Splits large documents into smaller overlapping chunks; Paragraphs -> sentences -> characters (if needed)
from langchain_chroma import Chroma
# A vector database that Stores: Embeddings
# Original text chunks
# Performs fast similarity search
from langchain_core.tools import tool


load_dotenv()

llm = ChatOpenAI(model = "gpt-5-nano", # lightweight version of GPT-5 for fast responses
                 temperature = 0) # determinstic outcomes

# Text to vector embeddings
# Embeddings are required for semantic search
embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small",
)

# PDF is the knowledge source for your RAG agent
pdf_path = "Stock_Market_Performance_2024.pdf"

# debugging purpose
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path) # loads the pdf

try:
    pages = pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages")

except Exception as e:
    print(f"Error loading pdf: {e}")
    raise

# Chunking process
# Creates a splitter object to divide documents into manageable chunks
# LLMs have context size limits
# Overlapping ensures context continuity between chunks, reducing hallucinations
# Makes semantic search more accurate because chunks are granular

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, # 1000 tokens splitting chunks
    chunk_overlap = 200 # overlap of 200 tokens
)

# Splits each page into multiple smaller Document objects
# page_content -> subset of text
# metadata -> original page number, source, etc
pages_split = text_splitter.split_documents(pages) # We now apply this to our pages
 

persist_directory = r"/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/LangGraph/Agent" # where ChromaDB will store its local files
collection_name = "stock_market" # the named collection inside the vector DB

if not os.path.exists(persist_directory):
    os.mkdir(persist_directory)
    
# Converts your chunks (pages_split) into embeddings using the embeddings model
try:
    vectorstore = Chroma.from_documents(
        documents=pages_split, # the chunked PDF pages
        embedding = embeddings, # embedding model instance (text-embedding-3-small)
        persist_directory=persist_directory, # where the database is saved on disk
        collection_name=collection_name # optional collection name inside ChromaDB
    )
    print(f"Created ChromaDB vector store!")

except Exception as e:
    print(f"Error setting up ChromaDB: {e}")
    raise

# Now we create our retriever
# Converts your vectorstore (ChromaDB) into a retriever object
# The retriever allows the LLM to query the vector store easily

""" 
1. Query embedding
2. Vector similarity search
3. Returning the most relevant document chunks
"""

retriever = vectorstore.as_retriever(
    search_type = "similarity", # retrieves chunks most similar to the query
    search_kwargs = {"k": 5} # K is the amounts of chunks to return
)

@tool
def retriever_tool(query: str) -> str: # Turns retrieval logic into a callable tool for the LLM
    """ This tool searches and returns the information from the Stock Market Performance 2024 Document """
    docs = retriever.invoke(query) # get top k chunks
    
    # Check if any results exist -> if none, return fallback message
    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 Document"
    
    # Return concatenated string of top matching documents
    results = []
    
    for i, doc in enumerate(docs):
        results.append(f"Doocument {i+1}: \n {doc.page_content}")
    
    return "\n\n".join(results)

tools = [retriever_tool]

llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages] # tells LangGraph how to combine messages when nodes update the state
    
""" 
1. Get the last message from state['messages']
2. Check if it has a tool_calls attribute
3. Check if any tool calls exist
4. Returns True -> agent should call the tool
5. Returns False -> no tools needed, can end or continue normal LLM reasoning
"""

def should_continue(state: AgentState):
    """ Check if the last message contains tools calls."""
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary for our tools

# LLM Agent
def call_llm(state: AgentState) -> AgentState: # Node that calls the LLM in the graph
    """ Function to call the LLM with the current state"""
    messages = list(state['messages'])
    # Provides context/instructions to the LLM
    messages = [SystemMessage(content = system_prompt)] + messages
    message = llm.invoke(messages) # LLM can now reason and optionally call tools
    return {"messages": [message]} # Returns a new state with the LLM message

# Retriever Agent
""" 
1. Reads tool_calls from last LLM message
2. Loops through each tool call
3. Checks if the tool exists in tools_dict
- If not -> returns error message
- If yes -> invokes tool with provided query
4. Wraps tool results in ToolMessage
5. Returns new state with tool messages
"""
def take_action(state: AgentState) -> AgentState: # Node that executes the tools requested by the LLM
    """ Execute tools from the LLM's response """
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        # query = extracted from the AIMessage’s tool_calls
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\n Tool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            
        
        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name = t['name'], content = str(result)))
    
    print("Tools Execution Complete. Back to the Model.")
    return {"messages": results} 

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)
graph.set_entry_point("llm")

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent",
        False: END,
    },
)
graph.add_edge("retriever_agent", "llm")


rag_agent = graph.compile()

def running_agent():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()

""" 
PDF has been loaded and has 9 pages
Created ChromaDB vector store!

=== RAG AGENT===

What is your question: What is the summary for Stock performance in 2024? Make a tabular format for each company and performance.
Calling Tool: retriever_tool with query: Stock Market Performance 2024 summary by company
Result length: 4876
Tools Execution Complete. Back to the Model.
Calling Tool: retriever_tool with query: Apple 2024 stock performance 2024 Magnificent 7 2024 performance
Result length: 4940
Calling Tool: retriever_tool with query: Microsoft 2024 stock performance 2024 Magnificent 7 2024 performance
Result length: 5005
Calling Tool: retriever_tool with query: Alphabet (Google) 2024 stock performance 2024 Magnificent 7
Result length: 4912
Calling Tool: retriever_tool with query: Amazon 2024 stock performance 2024 Magnificent 7
Result length: 5005
Calling Tool: retriever_tool with query: Meta 2024 stock performance 2024 Magnificent 7
Result length: 4978
Calling Tool: retriever_tool with query: Nvidia 2024 stock performance 2024 Magnificent 7
Result length: 4978
Calling Tool: retriever_tool with query: Tesla 2024 stock performance 2024 Magnificent 7
Result length: 4688
Tools Execution Complete. Back to the Model.
Calling Tool: retriever_tool with query: Microsoft 2024 stock performance 2024 Magnificent 7 2024 performance
Result length: 5005
Tools Execution Complete. Back to the Model.

=== ANSWER ===
Here’s a concise summary of stock performance in 2024, followed by a per-company table.

Summary of Stock Performance in 2024
- U.S. stock market was strong overall: S&P 500 total return about 25% for 2024 (price return around 23%). Nasdaq Composite rose about 29%. Smaller caps were more modest (S&P Equal-Weight and Russell 2000 around 10–11%). [Sources: Doocument 1]
- The rally was led by mega-cap tech stocks (the Magnificent 7). They surged on average about 64–67% in 2024 and accounted for roughly 54% of the S&P 500’s gains. [Sources: Doocument 5]

Tabular: 2024 Performance byCompany
- Apple Inc. (AAPL): +36% [Source: Doocument 1]
- Alphabet Inc. (Alphabet/Google): +~36% [Source: Doocument 1]
- Amazon.com Inc. (AMZN): +~48% [Source: Doocument 1]
- Meta Platforms, Inc. (META): +~72% [Source: Doocument 5]
- Tesla, Inc. (TSLA): +~63% [Source: Doocument 5]
- Microsoft Corp. (MSFT): Data not provided in the excerpts (Magnificent 7 note indicates overall group performance; individual MSFT figure not given) [Source: Doocument 5]
- Nvidia Corp. (NVDA): Data not provided in the excerpts (Magnificent 7 note includes NVDA as a member; individual figure not given) [Source: Doocument 5]

If you’d like, I can format the table with exact column alignment or add notes about the Magnificent 7’s total contribution versus individual stock performance if you provide the missing MSFT/NVDA figures or want me to pull those from the full document.

What is your question: Great, which one is best for investing if my budget is $420
Calling Tool: retriever_tool with query: best investment options under $420 budget stock market performance 2024 document
Result length: 4848
Tools Execution Complete. Back to the Model.

=== ANSWER ===
Short answer: The documents don’t label any specific investment as “the best” for a $420 budget. They only present market performance data for 2024, not product recommendations.

What the documents say
- The S&P 500 delivered roughly a 25% total return in 2024 (about +23% in price terms). This highlights the appeal of broad-market exposure during that year. (Stock Market Performance in 2024, Doocument 1)
- The Nasdaq Composite rose about 29% in 2024, indicating strong tech-led gains. (Stock Market Performance in 2024, Doocument 1)
- A group of mega-cap tech names, the “Magnificent 7” (Apple, Microsoft, Alphabet, Amazon, Meta, etc.), dominated performance. (Stock Market Performance in 2024, Doocument 1)

What this means for a $420 budget
- Since there’s no single “best stock” identified in the document, a broad, diversification-focused approach is sensible. The 2024 data shows the market largely moved higher with strength in the S&P 500 and tech leadership, but relying on a handful of stocks (mega-caps) can increase risk.
- A practical path aligned with the data would be to pursue broad-market exposure (e.g., an index ETF that tracks the S&P 500) rather than picking individual stocks. Your $420 could be used to buy fractional shares of such an ETF if your broker supports fractional trading, enabling you to gain broad market exposure within your budget.
- If you specifically want tech exposure (given the Magnificent 7’s influence), you could consider a small, diversified allocation to mega-cap names or a tech-focused ETF, but be mindful of concentration risk.

Citations to the source data
- S&P 500 ~25% total return in 2024: Stock Market Performance in 2024 (Doocument 1)
- Nasdaq Composite ~29% gain in 2024: Stock Market Performance in 2024 (Doocument 1)
- Magnificent 7 dominance: Stock Market Performance in 2024 (Doocument 1)

Would you like me to outline a simple, dollar-for-dollar example allocation for a $420 budget (e.g., a broad S&P 500 ETF with fractional shares) and note considerations (fees, risk, time horizon)?

What is your question: exit

"""