from random import random, choice, choices, randint

  # configs
DeadHNG = 50  # level of hunger that is lethal
AG = 3  # level of aggression that makes predator attack
HNG = 3  # level of hunger that makes animal eat


creatures = []


def rand_xy(n):  # generate random coordinates in field (n * n)
    return [int(n * random()), int(n * random())]


class Game:
    def __init__(self, f, num_of_cr):  # f — size of field (f*f)
        self.predators = [
            Predator(n, coordinates=rand_xy(f), age=0, mass=0, max_age=50,
                     aggression=5) for n in range(0, num_of_cr, 4)]  # id = 0 (
        # mod 4)
        self.preys = [
            Prey(n, coordinates=rand_xy(f), age=0, mass=0, max_age=50,
                 aggression=1) for n in range(1, num_of_cr, 4)]  # 1
        self.plants = [
            Plant(n, coordinates=rand_xy(f), age=0, mass=0, max_age=50,
                  aggression=choice([1, 2])) for n in range(2, num_of_cr, 4)]  # 2
        self.omni = [
            Omni(n, coordinates=rand_xy(f), age=0, mass=0, max_age=50,
                 aggression=4) for n in range(3, num_of_cr, 4)]  # 3
                 
        self.creatures = self.preys + self.predators + self.plants + self.omni
        global creatures
        for cr in self.creatures:
            creatures.append(cr)
        self.IdCoors = dict(zip([cr.id for cr in creatures],
                                [cr.xy for cr in creatures]))

    def shag(self):
        for cr in creatures:
            try:  # if cr is not a plant (plants cant move)
                cr.move()
                cr.get_hungry()
                cr.get_aged()
            except AttributeError:
                cr.grow()
                cr.get_aged()
        for id1 in range(len(self.creatures)):
            for id2 in range(id1 + 1, len(self.creatures)):
                try:
                    if self.IdCoors[id1] == self.IdCoors[id2]:
                        creatures[id1].interact(creatures[id2])
                except IndexError:
                    pass

    def run(self):
        day = 1
        while True:
            print(f'DAY {day}')
            self.shag()
            if not creatures:
                print('everyone died')
                break
            day += 1


class Creature:
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        self.id = num
        self.xy = coordinates
        self.x = self.xy[0]
        self.y = self.xy[1]
        self.age = age
        self.mass = mass
        self.max_age = max_age
        self.aggression = aggression

    def die(self):
        global creatures
        try:
            creatures.remove(self)
        except ValueError:  # creature already died in this shag
            pass

    def get_eaten(self, animal):
        animal.hungry = max(animal.hunger - self.mass, 0)
        print(f'{animal.species} {animal.id} ate {self.species} {self.id}')
        self.die()

    def get_aged(self):
        self.age += 1
        if self.age > self.max_age:
            self.die()
            print(f'{self.species} {self.id} died of age')


class Plant(Creature):
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        super().__init__(num, coordinates, age, mass, max_age, aggression)
        self.species = 'plant'

    def interact(self, another):
        if another.species in ['prey', 'omni'] and another.hunger > HNG:
            if self.aggression == 1:  # plant is not poison
                self.get_eaten(another)
            else:  # plant is poison
                chance = (1 - 1 / self.aggression)  # chance of intoxication
                action = choices([0, 1], weights=[1 - chance, chance])
                if action == [1]:  # intoxication
                    print(f'{another.id} tried to eat {self.id} and died '
                          f'from intoxication')
                    another.die()
                else:  # no intoxication
                    self.get_eaten(another)

    def grow(self):
        self.mass += 1


class Animal(Creature):
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        super().__init__(num, coordinates, age, mass, max_age, aggression)
        self.health = 10
        self.hunger = 0
        self.power = mass + aggression + self.hunger

    def move(self):
        stay_or_not = choice([0, 1])
        if stay_or_not == 1:
            direction = randint(1, 8)
            if direction == 1:
                self.y += 1
            elif direction == 2:
                self.x += 1
                self.y += 1
            elif direction == 3:
                self.x += 1
            elif direction == 4:
                self.y -= 1
                self.x += 1
            elif direction == 5:
                self.y -= 1
            elif direction == 6:
                self.y -= 1
                self.x -= 1
            elif direction == 7:
                self.x -= 1
            elif direction == 8:
                self.x -= 1
                self.y += 1

    def fight(self, another):  # winner eats loser
        lst = [self, another]
        winner = choices(lst, weights=[self.power, another.power])[0]
        lst.remove(winner)
        loser = lst[0]
        print(f'{another.id} and {self.id} had a fight, {winner.id} won')
        loser.get_eaten(winner)

    def fight_prey(self, prey):  # prey escapes if wins and dies else
        if self.hunger > HNG:
            chance = choices([0, 1], weights=[1 / self.hunger,
                                              1 - 1 / self.hunger])
            if chance[0] == 1:  # success attack
                prey.get_eaten(self)
            else:
                print(f'{self.id} unsuccessfully attacked {prey.id}')

    def get_hungry(self):
        self.hunger += 1
        if self.hunger >= DeadHNG:
            self.die()
            print(f'{self.species} {self.id} died because of hunger')


class Predator(Animal):
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        super().__init__(num, coordinates, age, mass, max_age, aggression)
        self.species = 'predator'

    def interact(self, other):
        if other.species == 'predator':
            if (self.hunger > AG and other.hunger > AG) or self.aggression > \
                    AG or other.aggression > AG:
                self.fight(other)
        elif other.species == 'prey':
            if self.aggression > AG or self.hunger > HNG:
                self.fight_prey(other)
        elif other.species == 'omni':
            if self.aggression > AG or self.hunger > HNG:
                self.fight(other)


class Omni(Animal):
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        super().__init__(num, coordinates, age, mass, max_age, aggression)
        self.species = 'omni'

    def interact(self, other):
        if other.species == 'predator':
            if (self.hunger > AG and other.hunger > AG) or self.aggression > \
                    AG or other.aggression > AG:
                self.fight(other)
        elif other.species == 'prey':
            if self.aggression > AG or self.hunger > HNG:
                self.fight_prey(other)
        elif other.species == 'omni':
            if self.aggression > AG or self.hunger > HNG:
                self.fight(other)
        elif other.species == 'plant':
            other.interact(self)


class Prey(Animal):
    def __init__(self, num, coordinates, age, mass, max_age, aggression):
        super().__init__(num, coordinates, age, mass, max_age, aggression)
        self.species = 'prey'

    def interact(self, other):
        if other.species == 'plant':
            other.interact(self)
        elif other.species in ['predator', 'omni']:
            other.fight_prey(self)


g1 = Game(int(input('how big is a spawn field?\n')), int(input('how many creatures?\n')))

g1.run()
