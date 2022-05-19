import pygame as pg


class Renderer:

    def __init__(self, game):
        self.gameObj = game
        self.screen = self.gameObj.window.screen
        self.dt = 0


    def render(self):
        self.gameObj.window.screen.fill("#00000000")

        self.sprites = self.gameObj.world.worldSprites
        for prio in self.gameObj.world.prio_sprites:
            for sprite in self.sprites:
                if sprite.spriteObj.state and sprite.spriteObj.priority == prio:
                    self.screen.blit(sprite.spriteObj.img, sprite.spriteObj.rect)

        self.dt = self.gameObj.window.mainClock.tick(self.gameObj.window.fps) / 1000.0
