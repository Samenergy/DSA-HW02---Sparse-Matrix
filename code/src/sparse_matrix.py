import os

class InvalidMatrixFormatException(Exception):
    pass

def read_sparse_matrix(file_path):
    sparse_matrix = {}
    try:
        with open(file_path, 'r') as file:
            rows_line = file.readline().strip()
            cols_line = file.readline().strip()
            
            if rows_line.startswith("rows="):
                num_rows = int(rows_line.split('=')[1])
            else:
                raise InvalidMatrixFormatException(f"Invalid format for rows in file {file_path}")
            
            if cols_line.startswith("cols="):
                num_cols = int(cols_line.split('=')[1])
            else:
                raise InvalidMatrixFormatException(f"Invalid format for cols in file {file_path}")
            
            for line in file:
                if line.strip():  # Ignore empty lines
                    parts = extract_numbers_from_line(line)
                    if len(parts) != 3:
                        print(f"Warning: Invalid line format: {line.strip()}")
                        continue
                    try:
                        row, col, value = map(int, parts)
                    except ValueError:
                        print(f"Warning: Invalid number format in line: {line.strip()}")
                        continue
                    
                    if row not in sparse_matrix:
                        sparse_matrix[row] = {}
                    sparse_matrix[row][col] = value
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except Exception as e:
        raise InvalidMatrixFormatException(f"An error occurred while reading the file {file_path}: {e}")
    
    return sparse_matrix

def extract_numbers_from_line(line):
    numbers = []
    num = ''
    for char in line:
        if char.isdigit() or char == '-':
            num += char
        else:
            if num:
                numbers.append(num)
                num = ''
    if num:
        numbers.append(num)
    return numbers

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def add_matrices(matrix1, matrix2):
    result = {}
    for row in matrix1:
        result[row] = {}
        for col in matrix1[row]:
            result[row][col] = matrix1[row].get(col, 0) + matrix2.get(row, {}).get(col, 0)
    for row in matrix2:
        if row not in result:
            result[row] = {}
        for col in matrix2[row]:
            if col not in result[row]:
                result[row][col] = matrix2[row][col]
    return result

def subtract_matrices(matrix1, matrix2):
    result = {}
    for row in matrix1:
        result[row] = {}
        for col in matrix1[row]:
            result[row][col] = matrix1[row].get(col, 0) - matrix2.get(row, {}).get(col, 0)
    for row in matrix2:
        if row not in result:
            result[row] = {}
        for col in matrix2[row]:
            if col not in result[row]:
                result[row][col] = -matrix2[row][col]
    return result

def multiply_matrices(matrix1, matrix2):
    result = {}
    for row1 in matrix1:
        for col1 in matrix1[row1]:
            for col2 in matrix2.get(col1, {}):
                if row1 not in result:
                    result[row1] = {}
                if col2 not in result[row1]:
                    result[row1][col2] = 0
                result[row1][col2] += matrix1[row1][col1] * matrix2[col1][col2]
    return result

def format_matrix(matrix):
    formatted = ""
    for row, cols in matrix.items():
        for col, value in cols.items():
            formatted += f"{row} {col} {value}\n"
    return formatted

def main():
    try:
        # Input the paths for input and output files
        input_path1 = input("Enter the path for the first matrix file: ").strip()
        input_path2 = input("Enter the path for the second matrix file: ").strip()
        output_path = input("Enter the path for the output file: ").strip()
        
        print(f"Reading matrix from {input_path1}")
        print(f"Reading matrix from {input_path2}")

        # Read the matrices from the specified files
        matrix1 = read_sparse_matrix(input_path1)
        matrix2 = read_sparse_matrix(input_path2)

        output_content = ""

        output_content += f"Matrix 1 ({input_path1}):\n"
        output_content += format_matrix(matrix1)

        output_content += f"\nMatrix 2 ({input_path2}):\n"
        output_content += format_matrix(matrix2)

        while True:
            print("\nChoose an operation:")
            print("1. Add matrix 1 and matrix 2")
            print("2. Subtract matrix 1 from matrix 2")
            print("3. Multiply matrix 1 by matrix 2")
            print("4. Exit")
            operation_choice = int(input("Enter your choice: "))

            if operation_choice == 1:
                result = add_matrices(matrix1, matrix2)
                print("Addition Result:")
                print(format_matrix(result))
                operation_name = "Addition Result"
            elif operation_choice == 2:
                result = subtract_matrices(matrix1, matrix2)
                print("Subtraction Result:")
                print(format_matrix(result))
                operation_name = "Subtraction Result"
            elif operation_choice == 3:
                result = multiply_matrices(matrix1, matrix2)
                print("Multiplication Result:")
                print(format_matrix(result))
                operation_name = "Multiplication Result"
            elif operation_choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose a number from 1 to 4.")
                continue

            output_content += f"\n{operation_name}:\n"
            output_content += format_matrix(result)

        # Write the output to the specified file
        write_to_file(output_path, output_content)
        print(f"Output saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
