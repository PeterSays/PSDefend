import random
from Interface import Interface, Die, Option, Counter
from Unit import Unit

class Team:
    def __init__(self, name, base: Unit, color=(0, 0, 0), other_color=(10, 10, 10), comp=False):
        self.comp = comp
        self.name = name
        self.base = base
        mapsiz = base.on_tile.mapsize
        mapyoff = base.on_tile.y_off
        self.mapyoff = mapyoff
        self.color = color
        self.other_color = other_color
        self.dice = [Die(self, round((mapsiz[0]*32)/2), mapyoff-30)]
        self.movepoints = 0
        self.movepoint_counter = Counter(f'{self.name}\'s Movepoints', self.dice[-1].x+32, self.mapyoff-33, 0, fontcolor=self.color)
        self.roll = 0
        self.members = []
        self.interfaces = []
        self.interfaces.extend(self.dice)
        self.interfaces.append(self.movepoint_counter)
        self.going = False
        self.done = True

    def add_dice(self, amt=1):
        for die_no in range(amt):
            new_die = Die(self, self.dice[-1].x+32, self.mapyoff-30)
            self.movepoint_counter.x = new_die.x+32
            self.dice.append(new_die)
            self.interfaces.append(new_die)
            if self.going:
                new_die.visible = True

    def turn_start(self):
        print(f'{self.name} started turn')
        self.going = True
        self.done = False
        self.movepoints = 0
        for inter in self.interfaces:
            inter.visible = True
        self.roll = 100

    def turn_end(self):
        print(f'{self.name} ended turn')
        self.done = True  # this is assumed, but it would not hurt to make sure
        self.going = False
        for inter in self.interfaces:
            inter.visible = False

    def routine(self):
        if self.roll:
            self.roll -= 1
            for die in self.dice:
                die.flip()
            if not self.roll:
                dicesum = sum([d.number for d in self.dice])
                self.movepoints += dicesum
                self.movepoint_counter.update_surf(dicesum)
        else:
            self.movepoint_counter.update_surf(self.movepoints)

