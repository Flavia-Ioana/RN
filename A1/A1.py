import pathlib
import math


def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line: 
                continue

            words = line.split()

            sign = 1
            r = [0.0, 0.0, 0.0]
            for word in words[:-2]:
                if word == '+':
                    sign = 1
                elif word == '-':
                    sign = -1
                else:                   
                    number = word[:-1]   
                    if number == '' or number == '+':
                       nr = 1.0
                    elif number == '-':
                       nr = -1.0
                    else:
                       nr = float(number)
                    
                    r['xyz'.index(word[-1])] = sign * nr + 0.0
                    sign = 1
                    
            A.append(r)

            B.append(float(words[-1]))
    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")



def determinant(matrix: list[list[float]]) -> float:
    a11, a12, a13 = matrix[0][0], matrix[0][1], matrix[0][2]
    a21, a22, a23 = matrix[1][0], matrix[1][1], matrix[1][2]
    a31, a32, a33 = matrix[2][0], matrix[2][1], matrix[2][2]
    return a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)

print(f"{determinant(A)=}")


 
def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")



def norm(vector: list[float]) -> float:
    return math.sqrt(sum(v ** 2 for v in vector))

print(f"{norm(B)=}")



def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

print(f"{transpose(A)=}")



def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]

print(f"{multiply(A, B)=}")



def modify_matrix(matrix, vector, index):
    m = [row[:] for row in matrix]
    for i in range(len(vector)):
        m[i][index] = vector[i]
    return m

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    
    if det_A == 0:
        return []

    Ax = modify_matrix(matrix, vector, 0)
    Ay = modify_matrix(matrix, vector, 1)
    Az = modify_matrix(matrix, vector, 2)

    x = determinant(Ax) / det_A
    y = determinant(Ay) / det_A
    z = determinant(Az) / det_A

    return [x, y, z]

print(f"{solve_cramer(A, B)=}")


def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    M = []
    for index, row in enumerate(matrix):
        if index != i:
            M.append(row[:j] + row[j+1:])
    return M

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cofactor_matrix = []
    for i in range(len(matrix)):
        cofactor_row = []
        for j in range(len(matrix)):
            M = minor(matrix, i, j)
            det_M = M[0][0] * M[1][1] - M[0][1] * M[1][0]
            cofactor_row.append(((-1) ** (i + j)) * det_M)
        cofactor_matrix.append(cofactor_row)
    return cofactor_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    cofactor_matrix = cofactor(matrix)
    return transpose(cofactor_matrix)

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    if det_A == 0:
        return []

    adj_A = adjoint(matrix)
    
    inv_A = [[adj_A[r][c] / det_A for c in range(len(adj_A))] for r in range(len(adj_A))]
    
    return multiply(inv_A, vector)

print(f"{solve(A, B)=}")