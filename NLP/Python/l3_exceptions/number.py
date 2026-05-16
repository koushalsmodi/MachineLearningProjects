while True:
    try:
        x = int(input("What's x? "))
        break
        
    # ValueError (int vs str)
    except ValueError:
        print("x is not an integer")
        
    # Try and else go hand in hand
    #else: 
        #break
    
print(f"x is {x}")