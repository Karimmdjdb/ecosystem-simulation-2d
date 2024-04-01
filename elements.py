#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:30:05 2023

@author: medjdou221
"""
import math
from utilities import *

class Element:
    __ids_count = 0
    
    @classmethod
    def get_ids_count(cls):
        return cls.__ids_count
    
    @classmethod
    def incr_ids_count(cls):
        cls.__ids_count += 1
    
    def __init__(self, name, char_repr, sprite = None, sprite_gender = None):
        self.__name = name
        Element.incr_ids_count()
        self.__id = Element.get_ids_count()
        self.__char_repr = char_repr
        if sprite_gender == None:
            self.__sprite = Sprite(sprite)
        else:
            self.__sprite = Sprite(sprite, gender=sprite_gender)
        self.__planet = None
        self.__sprite_coord = (0, 0)
        self.__grid_coord = (0, 0)
        self.__direction = (1, 1)
        self.__change_dir_timer = Timer(1)
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
    def get_char_repr(self):
        return self.__char_repr
    def get_sprite(self):
        return self.__sprite
    def set_planet(self, planet):
        self.__planet = planet
    def get_planet(self):
        return self.__planet
    def set_cord(self, x, y):
        self.__sprite_coord = (x, y)
    def get_cord(self):
        return self.__sprite_coord

    def update_sprite(self): # Change l'état du sprite
        self.__sprite.update_sprite()
    def update(self, surface, camera): # Met a jour a chaque frame l'élement
        self.draw(surface, camera)
    def aleatory_direction(self): # Change aléatoirement la direction
        new_x = self.__direction[0]
        new_y = self.__direction[1]
        change_x = random.randint(0, 500)
        change_y = random.randint(0, 500)
        if change_x < 3:
            new_x = random.randint(-1, 1)
        if change_y < 3:
            new_y = random.randint(-1, 1)
        self.__direction = (new_x, new_y)

    def target_direction(self, target): # Calcule la direction vers la cible
        x,y = 0, 0
        targx, targy = target.get_cord()
        if targx > self.get_cord()[0]:
            x = 1
        elif targx < self.get_cord()[0]:
            x = -1
        if targy+1 > self.get_cord()[1]:
            y = 1
        elif targy+1 < self.get_cord()[1]:
            y = -1
        self.__direction = (x, y)

    def escape_direction(self, danger): # Calcule la direction de fuite
        if self.__change_dir_timer.is_up():
            if danger.get_cord()[0] > self.get_cord()[0]:
                x = -1
            elif danger.get_cord()[0] < self.get_cord()[0]:
                x = 1
            else:
                x = random.randint(-1, 1)
            if danger.get_cord()[1] > self.get_cord()[1]:
                y = -1
            elif danger.get_cord()[1] < self.get_cord()[1]:
                y = 1
            else:
                y = random.randint(-1, 1)
            self.__direction = (x, y)

    # ----- Méthodes en rapport avec l'affichage et le mouvement
    def draw(self, surface, camera): # Affiche le sprite de l'element sur la surface
        surface.blit(self.__sprite.get_sprite_sheet(), (self.__sprite_coord[0]-camera.offset()[0], self.__sprite_coord[1]-camera.offset()[1]), (self.__sprite.get_offset()[0]*CELL_SIZE, self.__sprite.get_offset()[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    def move(self, speed): # Change les coordonnées et change la direction du sprite

        # Calcul des nouvelles coordonnées
        dist = speed
        new_x = self.__sprite_coord[0] + dist * self.__direction[0]
        new_y = self.__sprite_coord[1] + dist * self.__direction[1]

        # Vérififcation de dépassement
        if self.__planet != None :
            if new_y > (self.__planet.get_lines_count() * CELL_SIZE) - 1:
                new_y = (self.__planet.get_lines_count() * CELL_SIZE) - 1
            if new_y < 0:
                new_y = 0
            if new_x > (self.__planet.get_columns_count() * CELL_SIZE) - 1:
                new_x = (self.__planet.get_columns_count() * CELL_SIZE) - 1
            if new_x < 0:
                new_x = 0

        # Changement de la direction du sprite
        if new_x > self.__sprite_coord[0]:
            self.__sprite.change_direction("right")
        elif new_x < self.__sprite_coord[0]:
            self.__sprite.change_direction("left")
        else:
            if new_y > self.__sprite_coord[1]:
                self.__sprite.change_direction("up")
            if new_y < self.__sprite_coord[1]:
                self.__sprite.change_direction("down")

        #Activation/Désactivation de l'animation du sprite
        if new_x != self.__sprite_coord[0] or new_y != self.__sprite_coord[1]:
            self.__sprite.play()
        else:
            self.__sprite.stop()

        # Affectation des nouvelles coordonnées
        self.set_cord(new_x, new_y)

    def calc_distance(self, other): # Calcule la distance entre self et other
        if isinstance(other, Element):
            x = abs(other.get_cord()[0] - self.get_cord()[0])
            y = abs(other.get_cord()[1] - self.get_cord()[1])
            return math.sqrt(x**2 + y**2)

    def __repr__(self):
        return self.__char_repr

    def same(self, other):
        return type(self) == type(other)
    def __eq__(self, other):
        return type(self) == type(other) and self.get_id() == other.get_id()
class Ground(Element):
    
    def __init__(self):
        super().__init__('Ground', '\U0001F304')
class Resource(Element):
    
    def __init__(self, name, char_repr, sprite_path=None, value=0):
        super().__init__(name, char_repr, sprite_path)
        self.__value = value
    
    def get_value(self):
        return self.__value
    
    def __repr__(self):
        return super().__repr__() + ' (' + str(self.__value) + ')'
class Herb(Resource):
    
    def __init__(self):
        super().__init__('Herb', '\U0001F33F', HERB_PATH, 1)
class Water(Resource):
    def __init__(self):
        super().__init__('Water', '\U0001F30A', None, 2)
class Animal(Element):
    def __init__(self, name, char_repr, max_life, sprite_path, speed = 0, strength = 0):
        self.__gender = random.randint(0, 1)
        super().__init__(name, char_repr, sprite_path, sprite_gender=self.__gender)
        self.__age = 0
        self.__bar_life = [max_life, max_life]
        self.__strength = strength
        self.__speed = speed
        self.__danger = None
        self.__target = None
        self.__partner = None
        self.__verification_timer = Timer(1)
        self.__action_cooldown = CooldownTimer(2)
        self.__reproduction_cooldown = CooldownTimer(10)
        self.__reproduction_delay = CooldownTimer(2)
        self.__can_move = True
        self.__is_reproducing = False

    def update(self, surface, camera): # Redéfinition

        if self.is_dead():
            Messages.add_message(f"{self.get_name()} n°{self.get_id()} died.")
            self.get_planet().remove_animal(self)
        else:

            # Elements dans le champ de vision :
            view_field = [element for element in sorted(self.get_planet().get_elements(), key= lambda other : self.calc_distance(other)) if self.calc_distance(element)<=100 and self.get_id() != element.get_id()]

            # Prédateurs dans le champs de vision :
            predators = [element for element in view_field if issubclass(type(element), Animal) and element.is_predator(self)]

            # Proies dans le champs de vision :
            if issubclass(type(self), Carnivore):
                prey = [element for element in view_field if issubclass(type(element), Animal) and self.is_predator(element)]

            # Partenaires dans le champs de vision :
            partners = [element for element in view_field if self.same(element) and self.get_gender() != element.get_gender() and not element.__is_reproducing]

            # Resources dans le champs de vision :
            resources = ([element for element in view_field if type(element) == Water], [element for element in view_field if type(element) == Herb])


            # On vérifie si danger/target/partner existent toujours
            if self.__target not in view_field:
                self.__target = None
            if self.__danger not in view_field:
                self.__danger = None
            if self.__partner not in view_field:
                self.__partner = None
                self.__can_move = True

            # Recalcul de danger/target/partner toutes les x secondes
            if self.__verification_timer.is_up():
                if len(predators) != 0:
                    # Le danger est le prédateur le plus proche
                    self.__danger = predators[0]

                if issubclass(type(self), Carnivore) and len(prey) != 0:
                    # La cible est la proie la plus proche
                    self.__target = prey[0]
                if issubclass(type(self), Herbivore) and len(resources[1]) != 0:
                    self.__target = resources[1][0]

                if len(partners) != 0:
                    self.__partner = partners[0]



            if self.__danger != None:
                self.escape_direction(self.__danger)
            else:
                if self.__target != None:
                    self.target_direction(self.__target)
                    if self.calc_distance(self.__target) < 10 and self.__action_cooldown.is_up():
                        if issubclass(type(self), Carnivore):
                            self.attack(self.__target)
                            self.__action_cooldown.reset()
                            Messages.add_message(f"{self.get_name()} attacked {self.__target.get_name()} and caused him {self.__strength} damages !")
                        if issubclass(type(self), Herbivore):
                            self.get_planet().remove_resource(self.__target)
                            self.__action_cooldown.reset()
                            Messages.add_message(f"{self.get_name()} n°{self.get_id()} ate {self.__target.get_name()} n°{self.__target.get_id()}")
                else:
                    if self.__partner != None and self.__reproduction_cooldown.is_up() and self.__partner.__reproduction_cooldown.is_up():
                        self.target_direction(self.__partner)
                        if self.calc_distance(self.__partner) < 10 and self.__partner.__partner == self:
                            if not self.__is_reproducing and not self.__partner.__is_reproducing:
                                ReproductionGFX(((self.get_cord()[0]+self.__partner.get_cord()[0])//2, (self.get_cord()[1]+self.__partner.get_cord()[1])//2), 2)
                                self.__is_reproducing = True
                                self.__can_move = False
                                self.__reproduction_delay.reset()
                                self.__partner.__is_reproducing = True
                                self.__partner.__can_move = False
                                self.__partner.__reproduction_delay.reset()

                            if self.__is_reproducing and self.__reproduction_delay.is_up():
                                self.__can_move = True
                                self.__is_reproducing = False
                                self.__reproduction_cooldown.reset()
                                self.__partner.__can_move = True
                                self.__partner.__is_reproducing = False
                                self.__partner.__reproduction_cooldown.reset()
                                baby = type(self)()
                                self.get_planet().place_animal_at(baby, (self.get_cord()[0]+self.__partner.get_cord()[0])//2, (self.get_cord()[1]+self.__partner.get_cord()[1])//2)
                                Messages.add_message(f"new {baby.get_name()} was born !")
                    else:
                        self.aleatory_direction()

            if self.__can_move:
                self.move(self.__speed)
            else:
                self.get_sprite().stop()
            self.update_sprite()
            self.draw(surface, camera)
    
    def get_age(self):
        return self.__age

    def ageing(self):
        self.__age += 1
    
    def get_gender(self):
        return self.__gender

    def get_speed(self):
        return self.__speed
    
    def get_life_max(self):
        return self.__bar_life[1]
    
    def get_life(self):
        return self.__bar_life[0]
    
    def is_alive(self):
        if self.get_life() > 0:
            return True
        return False
    
    def is_dead(self):
        if self.is_alive() :
            return False
        return True
    
    def recovering_life(self, value):
        self.__bar_life[0] += value
        if self.__bar_life[0] > self.__bar_life[1]:
            self.__bar_life[0] = self.__bar_life[1]
    
    def losing_life(self, value):
        self.__bar_life[0] -= value
        if self.__bar_life[0] < 0:
            self.__bar_life[0] = 0

    def is_predator(self, target):
        if issubclass(type(self), Carnivore):
            return FoodChain.is_predator(self, target)
        return False

    def attack(self, other):
        other.losing_life(self.__strength)
class Herbivore(Animal):
    def __init__(self, name, char_repr, max_life, sprite_path, speed = 0, strength = 0):
        super().__init__(name, char_repr, max_life, sprite_path, speed, strength)
class Carnivore(Animal):
    def __init__(self, name, char_repr, max_life, sprite_path, speed = 0, strength = 0):
        super().__init__(name, char_repr, max_life, sprite_path, speed, strength)
class Mouse(Animal):
    
    def __init__(self):
        super().__init__('Mouse', '\U0001F42D', 2, MOUSE_PATH, 2)
class Lion(Carnivore):
    def __init__(self):
        super().__init__('Lion', '\U0001F981', 10, LION_PATH, 1, 2)
class Dragon(Carnivore):
    def __init__(self):
        super().__init__('Dragon', '\U0001F432', 20, DRAGON_PATH, 1, 3)
class Cow(Herbivore):
    def __init__(self):
        super().__init__('Cow', '\U0001F42E', 5, COW_PATH, .5)
class Camel(Herbivore):
    def __init__(self):
        super().__init__('Camel', '\U0001F42B', 5, CAMEL_PATH, .5)
class Rabbit(Herbivore):
    def __init__(self):
        super().__init__('Rabbit', '\U0001F430', 5, RABBIT_PATH, 2)


class FoodChain():

    __chain = {Dragon: [Mouse, Rabbit, Lion, Cow, Camel], Lion: [Mouse, Rabbit, Cow, Camel]}

    @classmethod
    def is_predator(cls, animal, target_animal):
        for prey in FoodChain.__chain[type(animal)]:
            if type(target_animal) == prey:
                return True
        return False