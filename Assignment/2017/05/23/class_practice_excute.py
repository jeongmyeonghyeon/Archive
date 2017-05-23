from class_practice import Whitehand, Something, Watching_tv, Play_game

chulsoo = Whitehand('철수', '남성', 30)

something = Something('무언가', '누군가', '어딘가')
waching_tv = Watching_tv('TV', '슬기', 'PC방')
play_game = Play_game('게임', '동혁', '집')

chulsoo.play(something)
chulsoo.play(waching_tv)
chulsoo.play(play_game)

print(chulsoo.age)
chulsoo.set_age = 25
print(chulsoo.get_age)