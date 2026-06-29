import json

base_dir = '/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/data/'
with open(base_dir + 'travelers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
def get_traveler(employee_id):
    for emp_id, emp_info in data.items():
        if emp_id == 'meta':
            pass
        
        if emp_id == employee_id:
            return emp_info

    return "No corresponding employee found at Company."
    
    
def get_traveler_tier(employee_id):
    for emp_id, emp_info in data.items():
        if emp_id == 'meta':
            pass
        
        if emp_id == employee_id:
            return emp_info['tier']

    return "No corresponding employee found at Company. Tier could not be determined."