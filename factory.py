# some examples of factory patterns in python
# calling PetStore makes an instance of DogFactory, which makes an instance of Dog; get_pet creates a specific pet


class Dog(object):
    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return 'dog'

    @staticmethod
    def speak():
        return 'woof'


class Cat(object):
    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return 'cat'

    @staticmethod
    def speak():
        return 'meow'


class DogFactory(object):
    @staticmethod
    def get_pet():
        return Dog()

    @staticmethod
    def get_food():
        return 'dog food'


class CatFactory(object):
    @staticmethod
    def get_pet():
        return Cat()

    @staticmethod
    def get_food():
        return 'cat food'


class PetStore(object):
    def __init__(self, pet_factory=None):
        self._pet_factory = pet_factory

    def show_pet(self):
        pet = self._pet_factory.get_pet()
        pet_food = self._pet_factory.get_food()

        print('The pet is a {}.'.format(pet))
        print('It says "{}!"'.format(pet.speak()))
        print('It eats {}.'.format(pet_food))


store = PetStore(DogFactory())
store.show_pet()


def get_pet(pet, name):
    pets = dict(dog=Dog(name), cat=Cat(name))
    return pets[pet]


d = get_pet('dog', 'Rover')
print('\n')
print('The {}\'s name is "{}".'.format(d.__str__(), d.name))
print('{} says "{}!"'.format(d.name, d.speak()))
