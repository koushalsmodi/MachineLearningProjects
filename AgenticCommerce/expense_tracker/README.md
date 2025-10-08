# 🧾 Expense Tracker (Python CLI)

## 📘 Overview
This is a simple **command-line expense tracker** written in Python.  
It allows users to:

- 📝 Add new expenses  
- 👀 View all expenses  
- 💰 Calculate the total amount spent  
- 💾 Save data persistently to a JSON file (`expenses.json`)  

When you run the program again, it automatically loads previously saved expenses,  
so you can continue from where you left off.

---

## 💾 Data Storage
Your data is saved automatically to a JSON file called **`expenses.json`** in this format:

```json
{
    "counter": 3,
    "expenses": {
        "1": {"description": "BMW", "amount": 42.0, "category": "Car"},
        "2": {"description": "MacBook", "amount": 11.0, "category": "Electronics"},
        "3": {"description": "T-Shirt", "amount": 10.0, "category": "Clothing"}
    }
}
