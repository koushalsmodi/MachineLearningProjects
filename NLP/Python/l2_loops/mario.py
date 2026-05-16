def main():
    # 2 rows and 4 cols
    print_shape(2, 4)
    

def print_shape(num_rows, num_cols):
    for _ in range(num_rows):
        print("#"*num_cols)
    
main()
    