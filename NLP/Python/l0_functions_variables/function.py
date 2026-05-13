def main():
    name = input("What's your name? ")
    hello(name)
    
def hello(to = "Someone"):
    print(f"hello, {to}")
    
if __name__ == "__main__":
    main()
    
    