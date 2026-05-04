import streamlit as st
import pandas as pd
import numpy as np
import joblib
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder
from scipy.stats import ttest_ind


# 1. Header — title and description
st.title('Fraud Explanation Assistant Dashboard')
st.write("Welcome to the User-Friendly Fraud Explanation Dashboard")

# 2. Load and clean data
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('cleaned_transactions.csv')
    le = LabelEncoder()
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))
    df_original = pd.read_csv('original_categories.csv')
    return df, df_original
    
# 3. Load model 
@st.cache_resource  
def load_model():
    return joblib.load('./xgboost_model.joblib')

# then calling them:
df, df_original = load_and_clean_data()
model = load_model()

# 4. Showing flagged transactions table
st.subheader("Flagged Transactions")

X = df.drop(columns = 'isFraud')

probabilities = model.predict_proba(X)[:, 1]
df['fraud_probability'] = probabilities 
filtered_df = df[df['fraud_probability'] > 0.5] 
""" 
display_cols = ['TransactionAmt', 'ProductCD', 'P_emaildomain', 'fraud_probability']
st.dataframe(filtered_df[display_cols])
"""
st.dataframe(data = filtered_df)

# 5. Selecting a transaction for investigation
st.subheader("Select a Transaction to Investigate")
selected_index = st.selectbox(
    "Choose a flagged transaction:",
    options=filtered_df.index.tolist()
)
single_transaction = filtered_df.loc[[selected_index]]

# 6. Showing risk score
risk_score = df.loc[selected_index, 'fraud_probability']
st.metric(label="Fraud Risk Score", value=f"{risk_score:.2%}")

# 7. Gemini explanation button

import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="fraudexplanationassistant", location="us-central1")
gemini_model = GenerativeModel('gemini-2.5-flash')

import shap
booster = model.get_booster()
explainer = shap.TreeExplainer(booster)

def single_transaction_analysis(single_transaction):
    single_transaction = single_transaction.drop(columns=['isFraud', 'fraud_probability'], errors='ignore')
    feature_names = single_transaction.columns
    fraud_probability = model.predict_proba(single_transaction)[:,1][0]
    
    shap_values = explainer.shap_values(single_transaction)
    single_shap = shap_values[0]
    
    shap_df = pd.DataFrame({
    'feature': feature_names,
    'shap_value': single_shap
    }).reindex(pd.Series(single_shap).abs().sort_values(ascending=False).index)


    prompt = f"""
    You are a Fraud Explanation Assistant at a financial institution. 
    Your task is to explain to a customer: clearly and calmly as to why their transaction was flagged as potentially unusual.

    Inputs:
    1. Fraud probability: {fraud_probability}
    2. Top 5 contributing factors (SHAP): {shap_df.head(5)}
    3. Transaction details:
        a. Amount: {single_transaction['TransactionAmt'].values[0]}
        b. Product: {df_original.loc[single_transaction.index, 'ProductCD'].values[0]}
        c. Email domain: {df_original.loc[single_transaction.index, 'P_emaildomain'].values[0]}
    
    Guidelines:
    1. Write only 2–3 concise sentences.
    2. Use a calm, reassuring, and non-accusatory tone.
    3. Do NOT say or imply the customer committed fraud.
    4. Avoid technical jargon
    5. Frame the explanation as a routine security precaution.
    6. Reference relevant factors such as transaction size, patterns, timing, or unusual activity if applicable.
    
    Context:
    1. Columns starting with "C" represent transaction count patterns.
    2. Columns starting with "V" represent risk signals.
    3. Columns starting with "D" represent time-related behavior.
    
    Goal:
    You MUST mention the specific transaction amount of {single_transaction['TransactionAmt'].values[0]} 
    and reference the specific risk factors identified above.
    Do not give a generic response.
    """
    response = gemini_model.generate_content(prompt)
    initial_explanation = response.text
    return initial_explanation, prompt
    
# initializing chat with transaction context when explanation is generated
if st.button("Generate Explanation"):
    explanation, prompt = single_transaction_analysis(single_transaction)
    st.session_state.explanation = explanation
    st.session_state.prompt = prompt
    st.session_state.messages = []
    st.session_state.chat = gemini_model.start_chat()
    st.session_state.chat.send_message(prompt)

# show explanation if it exists
if "explanation" in st.session_state:
    st.write(st.session_state.explanation)

    st.subheader("Fraud Assistant Chatbot")

    # display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # input box
    user_input = st.chat_input("Ask about this transaction...")

    if user_input:
        # add and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # get and display assistant response
        response = st.session_state.chat.send_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.write(response.text)