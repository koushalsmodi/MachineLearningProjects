import json

def main():
    
    all_products = {}
    product_counter = 1
    
    try:
        with open('products.json', 'r') as f:
            data = json.load(f)
            product_counter =  data.get("counter", 1)
            all_products = data.get("product", {})
            
    except FileNotFoundError:
        print("No exisiting file found")
    
    except json.JSONDecodeError:
        print("File exists but is empty or invalid. Starting fresh catalog.")

    while True:
        print("=== Product Catalog ===")
        print("1. View all products")
        print("2. Filter by category")
        print("3. Filter by price range")
        print("4. Add a new product")
        print("5. Save and Exit")
        
        try:
            user = int(input("Please choose an option: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        match user:
            case 1:
                view_all_products(all_products)
            
            case 2:
                filter_by_category(all_products)
                
            
            case 3:
                filter_by_price_range(all_products)
                
            case 4:
                product_counter = add_a_new_product(all_products, product_counter)
            
            case 5:
                save_and_exit(all_products, product_counter)
                
def view_all_products(all_products):
    
    if not all_products:
        print("No products to show yet")
        return 
    print("Viewing all products as follows")   

    for counter, each_product in all_products.items():
        each_product_name = each_product.get('each_product_name')
        each_product_category = each_product.get('each_product_category')
        each_product_price = each_product.get('each_product_price')
        each_product_stock = each_product.get('each_product_stock')
        
        print(f"{counter}. {each_product_name} - {each_product_category} - ${each_product_price:.2f} - In Stock: {each_product_stock}")
        
        

def filter_by_category(all_products):
    if not all_products:
        print("No products to show yet.")
        return 
    found = False
    print("Filter by category")   
    category_user = input("Category: ").strip().lower()
    print(f"For filter: {category_user}, here are the matches: ")
    
    for counter, each_product in all_products.items():
        each_product_category = each_product.get('each_product_category').strip().lower()
        
        if category_user == each_product_category:
            
            each_product_name = each_product.get('each_product_name')
            each_product_category = each_product.get('each_product_category')
            each_product_price = each_product.get('each_product_price')
            each_product_stock = each_product.get('each_product_stock')
            found = True
            print(f"{counter}. {each_product_name} - {each_product_category} - ${each_product_price:.2f} - In Stock: {each_product_stock}")
            
    if not found:
        print(f"No matches found for: {category_user}")
        
def filter_by_price_range(all_products):
    if not all_products:
        print("No products to show yet.")
        return 
    found = False
    print("Filter by price range")  
    price_user_low = float(input("Enter lower price for the range: $ "))
    price_user_high = float(input("Enter higher price for the range: $ "))
    
    print(f"For filter - low price: ${price_user_low} and high price: ${price_user_high}, here are the matches: ")
    for counter, each_product in all_products.items():
        each_product_price = each_product.get('each_product_price')
        
        if price_user_low <= each_product_price <= price_user_high:
            
            each_product_name = each_product.get('each_product_name')
            each_product_category = each_product.get('each_product_category')
            each_product_price = each_product.get('each_product_price')
            each_product_stock = each_product.get('each_product_stock')
            found = True
            print(f"{counter}. {each_product_name} - {each_product_category} - ${each_product_price:.2f} - In Stock: {each_product_stock}")
            
    if not found:
        print(f"No matches found between low price: {price_user_low} and high price: {price_user_high}") 
def add_a_new_product(all_products, product_counter):
    
    each_product = {}
    each_product_name = input("Enter product name: ")
    each_product_category = input("Enter category: ")
    each_product_price = float(input("Enter price: $ "))
    each_product_stock = int(input("Enter stock: "))
    
    each_product['each_product_name'] = each_product_name
    each_product['each_product_category'] = each_product_category
    each_product['each_product_price'] = each_product_price
    each_product['each_product_stock'] = each_product_stock
    
    all_products[product_counter] = each_product
    print(f"Product counter {product_counter} added successfully!")
    print(f"Product: {each_product_name} added successfully!")
    

    return product_counter + 1
    

def save_and_exit(all_products, product_counter):
    print("Saving changes...")
    data_to_save = {
        "counter": product_counter,
        "product": all_products
    }
    
    with open('products.json', 'w') as f:
        json.dump(data_to_save, f, indent = 4)
        
    print("Catalog saved to products.json")
    exit()
    
if __name__ == "__main__":
    main()