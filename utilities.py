from config import *
import pygame.image



class Camera:
    def __init__(self, vw, vh):
        self.wind_resolution = (vw, vh)
        self.__x_offset = 0
        self.__y_offset = 0
        self.__cursor = [pygame.image.load(GUI_CURS_PATH + "up_normal.png"), pygame.image.load(GUI_CURS_PATH + "left_normal.png"), pygame.image.load(GUI_CURS_PATH + "right_normal.png"), pygame.image.load(GUI_CURS_PATH + "down_normal.png"), pygame.image.load(GUI_CURS_PATH + "up_active.png"), pygame.image.load(GUI_CURS_PATH + "left_active.png"), pygame.image.load(GUI_CURS_PATH + "right_active.png"), pygame.image.load(GUI_CURS_PATH + "down_active.png"), pygame.image.load(GUI_CURS_PATH + "up_lock.png"), pygame.image.load(GUI_CURS_PATH + "left_lock.png"), pygame.image.load(GUI_CURS_PATH + "right_lock.png"), pygame.image.load(GUI_CURS_PATH + "down_lock.png")]

    def move(self, x, y):
        self.__x_offset += x
        self.__y_offset += y
        if self.__x_offset < 0:
            self.__x_offset = 0
        if self.__y_offset < 0:
            self.__y_offset = 0
        if self.__x_offset > (PLANET_LONGITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[0]:
            self.__x_offset = (PLANET_LONGITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[0]
        if self.__y_offset > (PLANET_LATITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[1]:
            self.__y_offset = (PLANET_LATITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[1]
    def offset(self):
        return (self.__x_offset, self.__y_offset)

    def cursor(self, camera_direction):
        return [self.__cursor[0+(camera_direction[0]*4)] if self.__y_offset != 0 else self.__cursor[8], self.__cursor[1+(camera_direction[1]*4)] if self.__x_offset != 0 else self.__cursor[9], self.__cursor[2+(camera_direction[2]*4)] if self.__x_offset != (PLANET_LONGITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[0] else self.__cursor[10], self.__cursor[3+(camera_direction[3]*4)] if self.__y_offset != (PLANET_LATITUDE_CELLS_COUNT + 1) * CELL_SIZE - self.wind_resolution[1] else self.__cursor[11]]


class Sprite:
    def __init__(self, path, is_mutant = True, gender = 0):
        if path != None:
            if not is_mutant:
                self.__sprite_sheet = pygame.image.load(f"{path}1.png")
            else:
                i = random.randint(0,10)
                if i == 0:
                    mutation = 3
                elif i == 1 or i == 2:
                    mutation = 2
                else:
                    mutation = 1
                self.__sprite_sheet = pygame.image.load(f"{path}{gender}_{mutation}.png")
        self.__xoff = 0
        self.__yoff = 0
        self.__tick = 0
        self.__play = False

    def play(self):
        self.__play = True
    def stop(self):
        self.__play = False
        self.__xoff = 0
        self.__tick = 0

    def get_sprite_sheet(self):
        return self.__sprite_sheet
    def update_sprite(self):
        if self.__play:
            if self.__tick == 0 :
                self.__xoff += 1
                self.__xoff = self.__xoff % 4
            self.__tick += 1
            self.__tick = self.__tick % 8
    def get_offset(self):
        return (self.__xoff, self.__yoff)

    def change_direction(self, direction):
        if direction == "up" :
            self.__yoff = 0
        if direction == "left" :
            self.__yoff = 1
        if direction == "right" :
            self.__yoff = 2
        if direction == "down" :
            self.__yoff = 3

class Timer:

    __all_timers = []
    @classmethod
    def get_timers(cls):
        return cls.__all_timers

    @classmethod
    def increase_all_timers(cls):
        for timer in cls.__all_timers:
            if type(timer) == Timer:
                timer.__time += 1
                timer.__time %= timer.__mod
            elif type(timer) == CooldownTimer:
                timer.__time += 1
                if timer.__time > timer.__mod - 1:
                    timer.__time = timer.__mod - 1

    def __init__(self, seconds):
        self.__mod = seconds * FPS
        self.__time = 0
        Timer.__all_timers.append(self)

    def is_up(self):
        if self.__time == self.__mod - 1:
            return True
        return False

    def reset(self):
        self.__time = 0

class CooldownTimer(Timer):
    def __init__(self, seconds):
        super().__init__(seconds)

class GFX:
    __all_gfx = []

    @classmethod
    def draw_all(cls, surface, camera):
        for gfx in cls.__all_gfx:
            if gfx.__delay.is_up():
                cls.__all_gfx.remove(gfx)

        for gfx in cls.__all_gfx:
            gfx.__sprite.update_sprite()
            surface.blit(gfx.__sprite.get_sprite_sheet(), (gfx.get_pos()[0]-camera.offset()[0], gfx.get_pos()[1]-camera.offset()[1]), (gfx.__sprite.get_offset()[0]*CELL_SIZE, gfx.__sprite.get_offset()[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def __init__(self, sprite_path, position, time = 1):
        self.__sprite = Sprite(sprite_path, False)
        self.__sprite.play()
        self.__position = position
        self.__delay = CooldownTimer(time)
        GFX.__all_gfx.append(self)

    def get_sprite(self):
        return self.__sprite

    def get_pos(self):
        return self.__position

class ReproductionGFX(GFX):
    def __init__(self, position, time = 1):
        super().__init__(GFX_PATH + "heart" , position, time)

class Messages():
    __last_messages = ["", "", ""]

    @classmethod
    def last_messages(cls):
        return cls.__last_messages
    @classmethod
    def add_message(cls, message):
        if len(cls.__last_messages) < 3:
            cls.__last_messages.append(message)
        else:
            cls.__last_messages[0] = cls.__last_messages[1]
            cls.__last_messages[1] = cls.__last_messages[2]
            cls.__last_messages[2] = message

class FireGFX(GFX):
    def __init__(self, position, time = 6):
        super().__init__(GFX_PATH + "fire" , position, time)