class Hanryang:
    '''놀고먹는 한량 생성 클래스'''
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        self.__hp = 5

    def hanryang_info(self):
        print("{}세 {} 한량, {} 이 생성됐습니다.(체력: {})".format(self.age, self.gender, self.name, self.hp))

    def play(self, anything):
        print("{}세 {}, {} 님이 ".format(self.age, self.gender, self.name))
        anything.play()

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, add_hp):
        self.__hp = add_hp

class Something:
    def __init__(self, name):
        self.name = name

    def play(self):
        print('{} 를 하고 논다.'.format(self.name))

class Watching_tv(Something):

    def play(self):
        print('{} 를 보고 논다.'.format(self.name))

class Play_game(Something):

    def play(self):
        print('{} 을 하고 논다.'.format(self.name))