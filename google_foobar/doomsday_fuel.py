# python 2.7

from fractions import Fraction

def solution(m):
    rMatrix, qMatrix = getSubs(m)

    result = []
    if len(rMatrix) == 0 and len(qMatrix) == 0:
        result = [0 for _ in range(len(m))]
        result[0] = 1
        result.append(1)
    else:
        result = calculate(rMatrix, qMatrix)
        result = finalize(result[0])

    return result


def finalize(nums):
    fractions = [Fraction(i).limit_denominator() for i in nums]
    cd = 1
    for i in fractions:
        if i.denominator != 1:
            cd = cd * i.denominator / findGcd(cd, i.denominator)
    cd = int(cd)

    nums = [int((i * cd).numerator) for i in fractions]
    nums.append(sum(nums))

    return nums


def findGcd(a, b):
    if b == 0:
        return a
    else:
        return findGcd(b, a % b)


def calculate(r, q):
    qSize = len(q)

    for row in range(len(r)):
        total = sum([x for x in r[row]] + [x for x in q[row]])
        r[row] = [float(x) / total for x in r[row]]
        q[row] = [float(x) / total for x in q[row]]

    i = buildIMatrix(qSize)
    result = subtract(i, q)
    result = inverse(result)

    result = dotProduct(result, r)

    return result


def determinant(m):
    if len(m) == 1:
        return m[0][0]

    result = 0
    for i in range(len(m)):
        sub = extract(m, 1, 0, len(m), -1, i)
        result += (-1) ** i * m[0][i] * determinant(sub)

    return result


def transpose(m):
    if len(m) == 0:
        return m
    result = []
    for column in range(len(m[0])):
        result.append([])
        for row in range(len(m)):
            result[column].append(m[row][column])

    return result


def adjugate(m):
    result = []
    for row in range(len(m)):
        result.append([])
        for column in range(len(m)):
            sub = extract(m, 0, 0, len(m), row, column)
            result[row].append((-1) ** (column + row) * determinant(sub))

    return transpose(result)


def inverse(m):
    det = determinant(m)
    if det == 0:
        det = 1

    adjM = adjugate(m)

    return [[y / det for y in x] for x in adjM]


def dotProduct(a, b):
    result = []
    for row in range(len(a)):
        result.append([])
        for column in range(len(b[row])):
            num = 0
            for index in range(len(a[row])):
                num += a[row][index] * b[index][column]
            result[row].append(num)

    return result


def extract(m, row, column, size, ignoreRow, ignoreColumn):

    result = []
    for i in range(row, min(row + size, len(m))):
        if i != ignoreRow:
            result.append([])
            for j in range(column, min(column + size, len(m[0]))):
                if j != ignoreColumn:
                    result[len(result) - 1].append(m[i][j])

    return result


def buildIMatrix(size):
    iMatrix = []
    for i in range(size):
        iMatrix.append([])
        for j in range(size):
            if (i == j):
                iMatrix[i].append(1)
            else:
                iMatrix[i].append(0)

    return iMatrix


def subtract(a, b):
    result = []
    for i in range(len(a)):
        result.append([])
        for j in range(len(a)):
            result[i].append(a[i][j] - b[i][j])

    return result


def getSubs(m):
    nonterminals = []
    terminals = []

    for row in range(len(m)):
        isTerminal = True
        for item in range(len(m[row])):
            if m[row][item] > 0:
                isTerminal = False
        if isTerminal:
            terminals.append(row)
        else:
            nonterminals.append(row)

    r = []
    q = []
    for row in nonterminals:
        r.append([m[row][x] for x in terminals])
        q.append([m[row][x] for x in nonterminals])

    return r, q


test = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [
    0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
print(solution(test))
