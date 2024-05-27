import os

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        self.elements = {}
        if file_path:
            self._load_from_file(file_path)
        elif num_rows and num_cols:
            self.rows = num_rows
            self.cols = num_cols
        else:
            raise ValueError("Either file_path or num_rows and num_cols must be provided")
    
    def _load_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            self.rows = int(lines[0].split('=')[1])
            self.cols = int(lines[1].split('=')[1])
            for line in lines[2:]:
                if line.strip():
                    self._parse_and_set_element(line)
    
    def _parse_and_set_element(self, line):
        print("Parsing line:", line)  # Debug print
        if line[0] != '(' or line[-1] != ')':
            raise ValueError("Input file has wrong format")
        try:
            row, col, value = map(int, line[1:-1].split(','))
            print("Parsed values:", row, col, value)  # Debug print
            self.set_element(row, col, value)
        except:
            raise ValueError("Input file has wrong format")

    
    def get_element(self, row, col):
        return self.elements.get((row, col), 0)
    
    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]
    
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, value)
        return result

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)
        return result

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        for (row, col), value in self.elements.items():
            for k in range(other.cols):
                result.set_element(row, k, result.get_element(row, k) + value * other.get_element(col, k))
        return result
    
    def to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (row, col), value in self.elements.items():
                f.write(f"({row}, {col}, {value})\n")

    def __str__(self):
        elements_str = '\n'.join([f"({row}, {col}, {value})" for (row, col), value in self.elements.items()])
        return f"rows={self.rows}\ncols={self.cols}\n{elements_str}"

def process_files(input_file_paths, output_file_path, operation):
    if len(input_file_paths) != 2:
        raise ValueError("There must be exactly two input files for the operation.")
    
    matrix1 = SparseMatrix(file_path=input_file_paths[0])
    matrix2 = SparseMatrix(file_path=input_file_paths[1])
    
    if operation == '1':
        result = matrix1 + matrix2
    elif operation == '2':
        result = matrix1 - matrix2
    elif operation == '3':
        result = matrix1 * matrix2
    else:
        raise ValueError("Invalid operation")

    result.to_file(output_file_path)
    print(f"Result written to {output_file_path}")

if __name__ == "__main__":
    input_file_paths = [
        "./sample_input_for_students/easy_sample_01_1.txt", 
        "./sample_input_for_students/easy_sample_01_2.txt",
        
    ]

    output_file_path = "./outputs/easy_sample_results_01.txt"

    operation = input("Select operation: 1 for addition, 2 for subtraction, 3 for multiplication: ").strip()

    process_files(input_file_paths, output_file_path, operation)
