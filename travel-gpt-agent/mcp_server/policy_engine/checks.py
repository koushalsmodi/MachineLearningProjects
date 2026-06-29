import json
from datetime import datetime

date_format = "%Y-%m-%d"


base_dir = '/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/data/'
with open(base_dir + 'policy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def check_cabin_class(tier, cabin_requested):
    cabin_class_response_dict = {'status': None, 'reason': None, 'details': None}
    cabin_hierarchy = ['economy', 'premium_economy', 'business']
    for tier_type, tier_details in data.items():
        if tier_type == 'meta':
            pass
        
        if tier_type == tier:
            tier_details_cabin_class = tier_details["cabin_class"]
            if cabin_hierarchy.index(cabin_requested) <= cabin_hierarchy.index(tier_details_cabin_class):
                cabin_class_response_dict['status'] = 'pass'
                cabin_class_response_dict['reason'] = 'Requested cabin is allowed for this tier'
                cabin_class_response_dict['details'] = f'Allowed cabin: {tier_details_cabin_class}'
                return cabin_class_response_dict
            else:
                cabin_class_response_dict['status'] = 'fail'
                cabin_class_response_dict['reason'] = 'Requested cabin is not allowed for this tier'
                cabin_class_response_dict['details'] = f'Allowed cabin: {tier_details_cabin_class}'
                return cabin_class_response_dict
    return {
        'status': 'fail',
        'reason': 'No corresponding tier found at company.',
        'details': None
    }


def check_approved_airline(tier, airline):
    approved_airline_response_dict = {'status': None, 'reason': None, 'details': None}
    for tier_type, tier_details in data.items():
        if tier_type == 'meta':
            pass
        
        if tier_type == tier:
            tier_details_airline = tier_details["approved_airlines"]
            if airline in tier_details_airline:
                approved_airline_response_dict['status'] = 'pass'
                approved_airline_response_dict['reason'] = 'Requested airline is allowed for this tier'
                approved_airline_response_dict['details'] = f'Allowed airline: {tier_details_airline}'
                return approved_airline_response_dict
            else:
                approved_airline_response_dict['status'] = 'fail'
                approved_airline_response_dict['reason'] = 'Requested airline is not allowed for this tier'
                approved_airline_response_dict['details'] = f'Allowed airline: {tier_details_airline}'
                return approved_airline_response_dict
    
    return {
        'status': 'fail',
        'reason': 'No corresponding tier found at company.',
        'details': None
    }       

def check_advance_booking(tier, departure_date):
    advance_booking_response_dict = {'status': None, 'reason': None, 'details': None}
    for tier_type, tier_details in data.items():
        if tier_type == 'meta':
            pass
        
        if tier_type == tier:
            tier_details_advance_booking_days = tier_details["advance_booking_days"]
            departure_date = datetime.strptime(departure_date, date_format)
            current_date = datetime.now()
            difference = departure_date - current_date 
            days_difference = difference.days
            
            if days_difference >= tier_details_advance_booking_days:
                advance_booking_response_dict['status'] = 'pass'
                advance_booking_response_dict['reason'] = 'Requested booking is allowed for this tier'
                advance_booking_response_dict['details'] = f'Allowed booking days: {tier_details_advance_booking_days}'
                return advance_booking_response_dict
            else:
                advance_booking_response_dict['status'] = 'fail'
                advance_booking_response_dict['reason'] = 'Requested booking is not allowed for this tier due to late booking'
                advance_booking_response_dict['details'] = f'Allowed booking days: {tier_details_advance_booking_days}'
                return advance_booking_response_dict
    
    return {
        'status': 'fail',
        'reason': 'No corresponding tier found at company.',
        'details': None
    }  

def check_upgrade_eligibility(tier, upgrade_cost):
    upgrade_eligibility_response_dict = {'status': None, 'reason': None, 'details': None}
    for tier_type, tier_details in data.items():
        if tier_type == 'meta':
                pass
            
        if tier_type == tier:
            tier_details_upgrade_eligibility = tier_details["upgrade_eligibility"]
            
            if tier_details_upgrade_eligibility is False:
                upgrade_eligibility_response_dict['status'] = 'fail'
                upgrade_eligibility_response_dict['reason'] = 'Requested upgrade is not allowed for this tier'
                upgrade_eligibility_response_dict['details'] = None
                return upgrade_eligibility_response_dict
            
            tier_details_max_upgrade_cost = tier_details["max_upgrade_cost"]
            
            if tier_details_upgrade_eligibility is True:
                if upgrade_cost <= tier_details_max_upgrade_cost:
                    upgrade_eligibility_response_dict['status'] = 'pass'
                    upgrade_eligibility_response_dict['reason'] = 'Requested upgrade is allowed for this tier'
                    upgrade_eligibility_response_dict['details'] = f'Allowed upgrade cost: {tier_details_max_upgrade_cost}'
                    return upgrade_eligibility_response_dict
                
                else:
                    upgrade_eligibility_response_dict['status'] = 'fail'
                    upgrade_eligibility_response_dict['reason'] = 'Requested upgrade is allowed for this tier but the cost is greater than max upgrade cost'
                    upgrade_eligibility_response_dict['details'] = f'Allowed upgrade cost: {tier_details_max_upgrade_cost}'
                    return upgrade_eligibility_response_dict
    
    return {
        'status': 'fail',
        'reason': 'No corresponding tier found at company.',
        'details': None
    }

def check_budget(tier, estimated_cost):
    budget_response_dict = {'status': None, 'reason': None, 'details': None}
    for tier_type, tier_details in data.items():
        if tier_type == 'meta':
            pass
        
        if tier_type == tier:
            tier_details_max_trip_budget = tier_details["max_trip_budget"]
            if estimated_cost <= tier_details_max_trip_budget:
                budget_response_dict['status'] = 'pass'
                budget_response_dict['reason'] = 'Requested budget is allowed for this tier'
                budget_response_dict['details'] = f'Allowed budget: {tier_details_max_trip_budget}'
                return budget_response_dict
                
            else:
                budget_response_dict['status'] = 'fail'
                budget_response_dict['reason'] = 'Requested budget is not allowed for this tier'
                budget_response_dict['details'] = f'Allowed budget: {tier_details_max_trip_budget}'
                return budget_response_dict
                
    return {
        'status': 'fail',
        'reason': 'No corresponding tier found at company.',
        'details': None
    }