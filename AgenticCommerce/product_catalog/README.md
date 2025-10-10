# 🛍️ Product Catalog Management System

A **command-line Python application** to manage a product catalog — allowing users to add, view, search, and filter products.  
The data is stored in a JSON file (`products.json`).

---

## 📋 Features

- **Add New Products**
  - Input product's: name, category, price, and stock quantity.
  - Automatically assigns a product ID using a counter.

- **View All Products**
  - Displays all products with formatted details.

- **Filter Products by Category**
  - Search products based on category name.
  - Case-insensitive matching for user convenience.

- **Filter Products by Price**
  - Search products based on price range (between low and high).

- **Persistent Storage**
  - All product data is saved in a JSON file (`products.json`).
  - The counter keeps track of the *next available product ID*.

- **Error Handling**
  - Graceful handling of missing or empty JSON files.
  - Prevents crashes when data is unavailable or malformed.

---

## 🧩 JSON File Structure

The `products.json` file stores data as follows:

```json
{
    "counter": 6,
    "product": {
        "1": {
            "each_product_name": "Water Bottle",
            "each_product_category": "Accessories",
            "each_product_price": 12.0,
            "each_product_stock": 50
        },
        "2": {
            "each_product_name": "Cricket bat",
            "each_product_category": "Sports",
            "each_product_price": 42.0,
            "each_product_stock": 200
        }
    }
}
```

---

## 🚀 How to Run

1. Make sure you have **Python 3.8+** installed.
2. Save your script as `product_catalog.py` and ensure it's in the same folder as (or will create) `products.json`.
3. Open your terminal in the project directory and run:

```bash
python3 product_catalog.py
```

---

## 📖 Example Usage

```
=== Product Catalog ===
1. View all products
2. Filter by category
3. Filter by price range
4. Add a new product
5. Save and Exit
```