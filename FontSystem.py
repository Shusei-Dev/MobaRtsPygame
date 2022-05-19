import pygame as pg


class FontClass:

    def __init__(self, gameObj):
        self.gameObj = gameObj
        self.textList = []

    def addText(self, text, font, size, color, pos):

        self.font = pg.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.textList.append((self.text, pos))

    def update(self, gameObj):
        self.gameObj = gameObj
        self.screen = self.gameObj.window.screen

        for text in self.textList:
            self.screen.blit(text[0], text[1])
