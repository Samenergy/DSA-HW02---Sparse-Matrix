class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, matrixFilePath=None):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}
        
        if matrixFilePath:
            self._read_from_file(matrixFilePath)
    
    def _read_from_file(self, filePath):
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()
                self.numRows = int(lines[0].split('=')[1])
                self.numCols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    if line.strip():
                        parts = line.strip().strip('()').split(',')
                        row = int(parts[0])
                        col = int(parts[1])
                        value = int(parts[2])
                        self.elements[(row, col)] = value
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filePath}")
        except Exception as e:
            raise ValueError("Input file has wrong format") from e
    
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
            result.setElement(row, col, value)
        
        for (row, col), value in other.elements.items():
            print(f"Adding element at ({row}, {col}): {value} + {result.getElement(row, col)}")
            result.setElement(row, col, value + result.getElement(row, col))
        
        return result
    
    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        
        result = SparseMatrix(self.numRows, self.numCols)
        
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value)
        
        for (row, col), value in other.elements.items():
            result.setElement(row, col, result.getElement(row, col) - value)
        
        return result
    
    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        
        result = SparseMatrix(self.numRows, other.numCols)
        
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                if (col1, col2) in other.elements:
                    value2 = other.getElement(col1, col2)
                    result.setElement(row1, col2, result.getElement(row1, col2) + value1 * value2)
        
        return result

    def save_to_file(self, filePath):
        with open(filePath, 'w') as file:
            file.write(f"rows={self.numRows}\n")
            file.write(f"cols={self.numCols}\n")
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")

def main():
    input_path1 = './sample_input_for_students/easy_sample_01_1.txt'
    input_path2 = './sample_input_for_students/easy_sample_01_2.txt'
    output_path = './outputs/result.txt'
    
    operation = input("Enter the operation (add, subtract, multiply): ").strip().lower()
    
    print(f"Reading matrix from {input_path1}")
    matrix1 = SparseMatrix(matrixFilePath=input_path1)
    print(f"Reading matrix from {input_path2}")
    matrix2 = SparseMatrix(matrixFilePath=input_path2)
    
    print(f"Matrix 1: {matrix1.numRows} x {matrix1.numCols}")
    print(f"Matrix 2: {matrix2.numRows} x {matrix2.numCols}")
    
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

