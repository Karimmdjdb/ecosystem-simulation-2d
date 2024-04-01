#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:30:24 2023

@author: medjdou221
"""
from elements import *

class PlanetAlpha():

    def __init__(self, name, longitude_cells_count, latitude_cells_count, ground):
        self.__longitude_cells_count = longitude_cells_count
        self.__latitude_cells_count = latitude_cells_count
        self.__name = name
        self.__elements = []
        self.__animals = []
        self.__current_animals_count = 0
        self.__resources = []
        self.__ground = ground

    def get_name(self):
        return self.__name

    def get_lines_count(self):
        return self.__latitude_cells_count

    def get_columns_count(self):
        return self.__longitude_cells_count

    # Elements gestion
    def get_elements(self):
        return self.__elements

    # Animals gestion
    def get_animals(self):
        return self.__animals
    def place_animals(self, animals):
        for animal in animals:
            x, y = self.get_random_place()
            if isinstance(animal, Animal):
                self.incr_current_animals_count()
                self.__elements.append(animal)
                self.__animals.append(animal)
                animal.set_cord(y * CELL_SIZE, x * CELL_SIZE)
                animal.set_planet(self)
    def place_animal_at(self, animal, x, y):
        self.incr_current_animals_count()
        self.__elements.append(animal)
        self.__animals.append(animal)
        animal.set_cord(x, y)
        animal.set_planet(self)
    def remove_animal(self, animal):
        self.decr_current_animals_count()
        self.__elements.remove(animal)
        self.__animals.remove(animal)
    def get_current_animals_count(self):
        return self.__current_animals_count
    def incr_current_animals_count(self):
        self.__current_animals_count += 1
    def decr_current_animals_count(self):
        self.__current_animals_count -=1

    # Resources gestion
    def get_resources(self):
        return self.__resources
    def place_resources(self, resources):
        for resource in resources:
            x, y = self.get_random_place()
            if isinstance(resource, Resource):
                self.__elements.append(resource)
                self.__resources.append(resource)
                resource.set_cord(y * CELL_SIZE, x * CELL_SIZE)
                resource.set_planet(self)
    def remove_resource(self, resource):
        self.__elements.remove(resource)
        self.__resources.remove(resource)

    def get_random_place(self):
        return (random.randint(0, self.get_lines_count()), random.randint(0, self.get_columns_count()))


    def get_line_str(self, line_number, separator):
        return separator.join([element.get_char_repr() for element in self.grid[line_number]])

    def get_grid_str(self, separator):
        return "\n".join([self.get_line_str(_, separator) for _ in range(self.get_lines_count())])