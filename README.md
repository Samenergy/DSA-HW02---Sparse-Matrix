Here's a simple README file for your sparse matrix operations project:

---

# Sparse Matrix Operations

## Description

This project allows you to perform operations (addition, subtraction, multiplication) on sparse matrices. Sparse matrices are matrices in which most elements are zero. The project reads two sparse matrices from input files, performs the specified operation, and writes the result to an output file.

## Folder Structure

```
DSA-HW02---Sparse-Matrix/
│
├── code/
│   ├── src/
│   │   └── sparse_matrix.py
│   └── outputs/
│       └── result.txt
│
├── sample_inputs/
│   ├── easy_sample_01_1.txt
│   └── easy_sample_01_2.txt
│
└── README.md
```

## Prerequisites

- Python 3.x

## Usage

1. Clone the repository:

```sh
git clone <repository-url>
```

2. Navigate to the project directory:

```sh
cd DSA-HW02---Sparse-Matrix
```

3. Ensure your input files are in the `sample_inputs` directory.

4. Run the script:

```sh
python code/src/sparse_matrix.py
```

5. Follow the prompts to select the operation and input files. The result will be saved to `code/outputs/result.txt`.

## Input File Format

The input files should have the following format:
- The first line specifies the number of rows.
- The second line specifies the number of columns.
- Each subsequent line specifies a non-zero element in the format `(row, column, value)`.

Example:
```
rows=3
cols=3
0 0 1
1 2 2
2 1 3
```

## Output

The result of the operation will be saved in `code/outputs/result.txt`.

## Example

Given two input files `easy_sample_01_1.txt` and `easy_sample_01_2.txt`, the script will perform the selected operation and save the result in `result.txt`.

## Notes

- Ensure the matrices conform to the mathematical rules for the selected operation.
- Handle file paths and ensure input files exist in the specified directory.

## License

This project is licensed under the MIT License.

