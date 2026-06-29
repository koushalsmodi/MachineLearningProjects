import json

base_dir = '/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/data/'
with open(base_dir + 'budgets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
def get_remaining_budget(team_entered):
    for team, team_budget in data.items():
        if team == 'meta':
            pass
        
        if team == team_entered:
            return team_budget['remaining_budget']
        
    return "No team found at Company"
        
def deduct_budget(team_entered, amount):
    for team, team_budget in data.items():
        if team == 'meta':
            pass
        
        if team == team_entered:
            if amount <= team_budget['remaining_budget']:
                remaining = team_budget['remaining_budget'] - amount
                data[team_entered]['remaining_budget'] = remaining
                
                with open(base_dir + 'budgets.json', "w", encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                    
                return {
                    "status": "success",
                    "remaining_budget": remaining
                }
                
            else:
                return "Estimated cost is above remaining budget"
    
    
        
    return "No team found at Company"