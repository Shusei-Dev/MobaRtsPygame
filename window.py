import pygame as pg
from pygame.locals import *

class Window:

    def __init__(self, game):
        '''Create the pygame window and init the gameloop'''
        pg.init()

        self.gameObj = game

        self.game_size = (1280, 720)
        self.screen_size = (pg.display.Info().current_w, pg.display.Info().current_h)
        self.screen = pg.display.set_mode(self.game_size)

        self.fps = 60
        self.showFps = False
        self.mainClock = pg.time.Clock()

        self.gameName = "GestionGame"
        self.gameVersion = 0.1
        pg.display.set_caption(self.gameName + str(self.gameVersion))

        self.running = True
        self.spriteList = []

    def update(self, gameObj):
        self.gameObj = gameObj
        self.screen.flip()

