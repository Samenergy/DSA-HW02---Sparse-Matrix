class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, matrixFilePath=None):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}  # Use a dictionary to store non-zero elements

        if matrixFilePath:
            self._read_from_file(matrixFilePath)
    
    def _read_from_file(self, filePath):
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()
                # Process number of rows and columns
                self.numRows = int(self._extract_number(lines[0]))
                self.numCols = int(self._extract_number(lines[1]))

                # Process matrix elements
                for line in lines[2:]:
                    if line.strip():  # Ignore empty lines
                        elements = line.strip()[1:-1].split(',')
                        row, col, value = int(elements[0]), int(elements[1]), int(elements[2])
                        self.elements[(row, col)] = value
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filePath}")
        except Exception as e:
            raise ValueError("Input file has wrong format") from e
    
    def _extract_number(self, line):
        number = ''
        for char in line:
            if char.isdigit():
                number += char
        return number
    
    def getElement(self, row, col):
        if 0 <= row < self.numRows and 0 <= col < self.numCols:
            return self.elements.get((row, col), 0)
        else:
            raise IndexError("Row or column index out of bounds")
    
    def setElement(self, row, col, value):
        if 0 <= row < self.numRows and 0 <= col < self.numCols:
            if value != 0:
                self.elements[(row, col)] = value
            elif (row, col) in self.elements:
                del self.elements[(row, col)]
        else:
            raise IndexError("Row or column index out of bounds")
    
    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for addition")

        result = SparseMatrix(self.numRows, self.numCols)
        
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value + other.getElement(row, col))

        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.setElement(row, col, value)

        return result
    
    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for subtraction")

        result = SparseMatrix(self.numRows, self.numCols)
        
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value - other.getElement(row, col))

        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.setElement(row, col, -value)

        return result
    
    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions do not match for multiplication")

        result = SparseMatrix(self.numRows, other.numCols)
        
        for i in range(self.numRows):
            for j in range(other.numCols):
                value = 0
                for k in range(self.numCols):
                    value += self.getElement(i, k) * other.getElement(k, j)
                if value != 0:
                    result.setElement(i, j, value)

        return result

    def save_to_file(self, filePath):
        with open(filePath, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")

def main():
    # Specify the paths for input and output files
    input_path1 = './sample_inputs/easy_sample_01_1.txt'
    input_path2 = './sample_inputs/easy_sample_01_2.txt'
    output_path = './outputs/result.txt'
    
    # Prompt user for the operation
    operation = input("Enter the operation (add, subtract, multiply): ").strip().lower()
    
    print(f"Reading matrix from {input_path1}")
    print(f"Reading matrix from {input_path2}")
    
    matrix1 = SparseMatrix(matrixFilePath=input_path1)
    matrix2 = SparseMatrix(matrixFilePath=input_path2)
    
    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation. Please enter 'add', 'subtract', or 'multiply'.")
        return

    print(f"Saving result to {output_path}")
    result.save_to_file(output_path)
    print(f"Resulting matrix saved to {output_path}")

if __name__ == '__main__':
    main()
