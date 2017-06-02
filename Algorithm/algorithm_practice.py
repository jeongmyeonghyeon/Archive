def rm_small(mylist):
    # 함수를 완성하세요
    lowest_num_idx = 0
    for i in range(len(mylist) - 1):
        if mylist[lowest_num_idx] > mylist[i + 1]:
            lowest_num_idx = mylist.index(mylist[i + 1])

    del mylist[lowest_num_idx]
    return mylist


# 아래는 테스트로 출력해 보기 위한 코드입니다.
my_list = [4, 3, 2, 1]
print("결과 {} ".format(rm_small(my_list)))
