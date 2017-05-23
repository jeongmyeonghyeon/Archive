class Whitehand:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.__age = age

    def play(self, anything):
        print("{}세 {}, {}이/가 ".format(self.__age, self.gender, self.name))
        anything.play()

    @property
    def age(self):
        return self.__age

    @age.setter
    def set(self, new_age):
        self.__age = new_age

class Something:
    def __init__(self, name, friend, place):
        self.name = name
        self.friend = friend
        self.place = place

    def play(self):
        print('{}와 {}에서 {} 을/를 하고 논다.'.format(self.friend, self.place, self.name))

class Watching_tv(Something):

    def play(self):
        print('{}와 {}에서 {} 을/를 보고 논다.'.format(self.friend, self.place, self.name))

class Play_game(Something):

    def play(self):
        print('{}와 {}에서 {} 을/를 하고 논다.'.format(self.friend, self.place, self.name))