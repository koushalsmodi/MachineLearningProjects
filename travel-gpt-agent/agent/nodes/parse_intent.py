from datetime import datetime
import sys
import json
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage


base_dir = '/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/agent/prompts/'


def make_parse_intent_node(model):
    def parse_intent(state: AgentState) -> AgentState:
        with open(base_dir + 'parse_intent.txt', 'r') as f:
            system_prompt = f.read()
            today_str = datetime.today().strftime('%Y-%m-%d')
            system_prompt = system_prompt.replace('{today_date}', today_str)
            # print(system_prompt)

        sys_msg = SystemMessage(content=system_prompt)
        human_msg = HumanMessage(content = state['messages'][-1].content)
        messages = [sys_msg, human_msg]

        response = model.invoke(messages)
        response = response.content
        start = response.find('{')
        end = response.rfind('}') + 1
        clean_json = response[start:end]
        parsed = json.loads(clean_json)
        return {
                "employee_id": parsed['employee_id'],
                "origin": parsed['origin'],
                "destination": parsed['destination'],
                "departure_date": parsed['departure_date'],
                "cabin_preference": parsed['cabin_preference']
        }
    return parse_intent