import json

def main():
    all_expenses = {}
    expense_counter = 1
    
    try:
        with open("expenses.json", "r") as f:
            data = json.load(f)
            expense_counter = data.get("counter", 1)
            all_expenses = data.get("expenses", {})
    except FileNotFoundError:
        print("No existing expense file found")
    
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View total")
        print("4. Exit")
        try:
            user_input = int(input("Please choose one of the options: "))
            
        except ValueError:
            print("Invalid input! Please enter a number between 1-4.")
            continue

        match user_input:
            case 1:
                expense_counter = add_expense(all_expenses, expense_counter)
            case 2:
                view_expenses(all_expenses)
            case 3:
                view_total(all_expenses)
            case 4:
                user_exit(all_expenses, expense_counter)
                break
            case _:
                print("Invalid option. Please choose between 1-4.")


def add_expense(all_expenses, expense_counter):
    each_expense = {}
    description = input("Description: ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return expense_counter

    category = input("Category: ")
    each_expense['description'] = description
    each_expense['amount'] = amount
    each_expense['category'] = category

    all_expenses[expense_counter] = each_expense
    print(f"Expense #{expense_counter} added successfully")
    return expense_counter + 1 

def view_expenses(all_expenses):
    if not all_expenses:
        print("No expenses to show yet.")
        return

    print("\n--- All Expenses ---")
    for expense_num, each_expense in all_expenses.items():
        description = each_expense.get('description')
        amount = each_expense.get('amount')
        category = each_expense.get('category')
        print(f"{expense_num}. Description: {description}, Amount: ${amount:.2f}, Category: {category}")
    

def view_total(all_expenses):
    if not all_expenses:
        print("No expenses to total yet.")
        return

    total = sum(each_expense.get('amount', 0) for each_expense in all_expenses.values())
    print(f"Total expenses: ${total:.2f}")
            
def user_exit(all_expenses, expense_counter):
    prompt = input("Save data before exiting? (Y/n): ")
    if prompt.strip().lower() in ['y', 'yes']:
        print("Saving...")
        
        data_to_save = {
            'counter': expense_counter,
            'expenses': all_expenses
        }
        
        with open("expenses.json", "w") as f:
            json.dump(data_to_save, f)

        print("Saved successfully")

    else:
        print("Exiting without saving")
    
    exit()
    
if __name__ == "__main__":
    main()