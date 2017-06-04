def nextSqure(n):
    sqrt = n ** (1 / 2)

    if sqrt % 1 == 0:
        result = int((sqrt + 1) ** 2)
        return result
    return 'no'

print(nextSqure(121))