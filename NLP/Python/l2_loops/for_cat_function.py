def main():
    n = get_num()
    meow(n)
    
def get_num():
    while True:
        n = int(input("What's n? "))
        if n > 0:
            return n
    

def meow(n):
    for _ in range(n):
        print("meow")
        
main()