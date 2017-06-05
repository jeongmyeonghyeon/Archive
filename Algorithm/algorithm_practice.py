def sum_digit(number):
    '''number의 각 자릿수를 더해서 return하세요'''
    result = 0
    split_number = map(int, str(number))
    for i in split_number:
        result += i
    return result


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(sum_digit(7569)))
