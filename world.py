import pygame as pg
from Sprites.sprite import *
from Sprites.EntityClass import *
from Sprites.PlayerClass import *
import random

class World:

    def __init__(self, game):

        self.gameObj = game
        

        # --Initialize all the class--
        self.spriteClass = Sprite(self.gameObj)
        self.entityClass = EntityClass(self.gameObj)

        self.worldSprites = []

        self.assets = self.gameObj.assets

    def addSpritestoList(self, spriteList):
        for sprite in spriteList:
            if sprite not in self.worldSprites:
                self.worldSprites.append(sprite)

    def test(self):
        # -- Test --
        self.player = PlayerClass(self.gameObj, self.assets.playerTest, (0, 0), True, 1)

    def update(self, gameObj):
        self.gameObj = gameObj

        self.addSpritestoList(self.entityClass.entityList)

        self.dt = self.gameObj.renderer.dt

        self.spriteClass.update(self.gameObj)
        self.entityClass.update(self.gameObj)

        self.player.update(self.gameObj)

        for sprite in self.worldSprites:
            sprite.update(self.gameObj)
