from class_practice import Hanryang, Something, Watching_tv, Play_game

print("안녕하세요? 놀기에 앞서 몇가지 묻겠습니다.")
hanryang_name = input("이름?: ")
hanryang_gender = input("성별: ")
hanryang_age = input("나이?: ")

# 입력된 정보로 한량 생성
new_hanryang = Hanryang(hanryang_name, hanryang_gender, hanryang_age)
# 생성된 한량 정보 확인
new_hanryang.hanryang_info()

# 한량의 체력이 남아있으면 놀이 선택 반복 출력
while new_hanryang.hp:
    print("뭘 하고 놀까요? 번호를 선택해주세요")
    select_num = input("1.무언가 2.티비보기 3.게임하기 0. 그만놀기: ")
    if select_num == '1':
        some = Something('무언가')
        new_hanryang.play(some)
        new_hanryang.hp -= 1
        print('현재 체력: {}'.format(new_hanryang.hp))
    elif select_num == '2':
        tv = Watching_tv('티비')
        new_hanryang.play(tv)
        new_hanryang.hp -= 1
        print('현재 체력: {}'.format(new_hanryang.hp))
    elif select_num == '3':
        game = Play_game('게임')
        new_hanryang.play(game)
        new_hanryang.hp -= 1
        print('현재 체력: {}'.format(new_hanryang.hp))
    elif select_num == '0':
        print('내일도 놀아요')
        break
    elif select_num == '':
        print("보기의 번호를 선택해주세요")
    else:
        print("보기의 번호를 선택해주세요")
else:
    print('쉬고나서 다시 놀아요')