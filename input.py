import pygame as pg
from pygame.locals import *

class Input:

    def __init__(self, game):

        self.gameObj = game
        self.inputList = {"z": False, "q": False, "s": False, "d": False, "up": False, "down": False, "left": False, "right" : False}

    def update(self):
        self.event()
        pg.display.flip()

    def event(self):
        self.mouse_left, self.mouse_middle, self.mouse_right = pygame.mouse.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameObj.window.running = False

            if event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.gameObj.window.running = False

                if pg.key.name(event.key) in self.inputList.keys():
                    self.inputList[pg.key.name(event.key)] = True

            if event.type == pg.KEYUP:
                if pg.key.name(event.key) in self.inputList.keys():
                    self.inputList[pg.key.name(event.key)] = False

    def get(self, keyValue):

        return self.inputList[keyValue]


    def is_wasd_input(self):
        for key in self.inputList:
            if self.inputList[key]:
                return True

        return False
