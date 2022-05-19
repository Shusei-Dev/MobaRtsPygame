import pygame as pg
from pygame.locals import *

class Input:

    def __init__(self, game):

        self.gameObj = game
        self.inputList = {"y": False, "up": False, "down": False, "right": False, "left": False}

    def update(self):
        self.event()
        pg.display.flip()

    def event(self):
        self.mouse_left, self.mouse_middle, self.mouse_right = pg.mouse.get_pressed()
        self.mouse_pos_clicked = pg.mouse.get_pos()

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
