from random import *

def generate_zero_configuration(n):
    matrix = [[1 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        col = randint(0, n - 1)
        matrix[i][col] = 0
    
    for j in range(n):
        row = randint(0, n - 1)
        matrix[row][j] = 0
    
    row_idx_1 = randint(0, n - 1)
    row_idx_2 = randint(0, n - 1)

    while row_idx_1 == row_idx_2:
        row_idx_2 = randint(0, n - 1)
    
    bad_row = [1] * n
    zero_pos = randint(0, n - 1)
    bad_row[zero_pos] = 0
    matrix[row_idx_1] = bad_row
    matrix[row_idx_2] = bad_row

    for j in range(n):
        if(j == zero_pos):
            continue
        new_zero_idx = randint(1, n - 1)
        while(new_zero_idx == row_idx_1 or new_zero_idx == row_idx_2):
            new_zero_idx = randint(1, n - 1)

        matrix[new_zero_idx][j] = 0

    return matrix

def generate_matrix(n, min_val = 1, max_val = 100):
    matrix = generate_zero_configuration(n)
    random_zero_num = randint(min_val, max_val // 2)
    result = []
    for row in matrix:
        new_row = []
        for value in row:
            if value == 0:
                new_row.append(random_zero_num)
            else:
                new_row.append(randint(random_zero_num + 1, max_val))
        result.append(new_row)
    return result

def print_matrix(matrix):
    for row in matrix:
        print(*row)

def main():
    matrix = generate_matrix(5)
    print_matrix(matrix)

if __name__ == "__main__":
    main()