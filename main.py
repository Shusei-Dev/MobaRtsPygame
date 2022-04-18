import pygame as pg
from window import *
from assets import *
from renderer import *
from input import *
from world import *


class Game:

    def __init__(self):

        self.window = Window(self)
        self.input = Input(self)
        self.assets = Assets()
        self.renderer = Renderer(self)
        self.world = World(self)
        self.world.init_world(self.assets.mapTest)
                
    def update(self):

        self.input.update()
        self.world.update(self)
        self.renderer.render()

    def run(self):
        while self.window.running:
            self.update()



if __name__ == "__main__":
    game = Game()
    game.run()
