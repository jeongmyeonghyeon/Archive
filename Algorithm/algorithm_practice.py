def gcdlcm(a, b):
    yaksoo_a = []
    yaksoo_b = []
    for i in range(a):
        if a % (i+1) == 0:
            yaksoo_a.append(i+1)
    for i in range(b):
        if b % (i+1) == 0:
            yaksoo_b.append(i+1)

    return yaksoo_b

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(gcdlcm(3,12))