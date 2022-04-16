import pygame as pg


class Sprite(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        self.gameObj = game

        self.spriteType = ["tile", "entity", "background"]
        self.spriteList = []

        self.surface = self.gameObj.window.screen

    def newSprite(self, name, img, pos, type, prio, state=bool(), col_box_size=None, col_box_pos=None, size=None):
        self.spriteObj = NewSprite(self, name, img, pos, type, state, prio, col_box_size, col_box_pos, size)
        self.spriteList.append(self.spriteObj)
        return self.spriteObj

    def update(self, gameObj):
        self.gameObj = gameObj
        self.prio_sprites = []
        self.prio = 0
        while len(self.prio_sprites) != len(self.spriteList):
            for sprite in self.spriteList:
                if sprite.priority == self.prio:
                    self.prio_sprites.append(sprite)

            self.prio += 1


class NewSprite(pg.sprite.Sprite):

    def __init__(self, spriteClass, name, img, pos, type, prio, state=bool(), col_box_size=None, col_box_pos=None, size=None):
        self.spriteList = []

        self.pos = pos
        self.posX, self.posY = pos[0], pos[1]

        if type in spriteClass.spriteType:
            self.type = type

        self.name = name
        self.img = self.import_image(img)
        self.origine_img = self.img
        self.state = state

        self.rect = self.img.get_rect()
        self.rect.topleft = (self.posX, self.posY)

        if size == None:
            self.size = self.get_sprite_size()
        else:
            self.size = size

        self.priority = prio

        if col_box_size != None and col_box_pos != None:

            self.is_colision, self.col_state = True, True

            self.show_col = False

            self.colision_box_size = col_box_size
            self.colision_box_pos = col_box_pos

            if not self.colision_box_size < self.size:
                if self.colision_box_pos[0] > 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] >= 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] > 0 and self.colision_box_pos[1] >= 0:
                    self.new_size = ((self.colision_box_size[0] + self.size[0]) - (self.size[0] - self.colision_box_pos[0]), (self.colision_box_size[1] + self.size[1]) - (self.size[1] - self.colision_box_pos[1]))
                    self.new_img = pg.Surface(self.new_size)

            if self.colision_box_pos[0] < 0 and self.colision_box_pos[1] >= 0:
                self.new_size = ((self.colision_box_size[0] + self.size[0]) - self.colision_box_pos[0], (self.colision_box_size[1] + self.size[1]) - self.colision_box_pos[1])
                self.new_img = pg.Surface(self.new_size)

            if self.colision_box_pos[0] >= 0 and self.colision_box_pos[1] < 0:
                self.new_size = ((self.colision_box_size[0] + self.size[0]) - (self.size[0] - self.colision_box_pos[0]), (self.colision_box_size[1] + self.size[1]) - (self.size[1] - self.colision_box_pos[1]))
                self.new_img = pg.Surface(self.new_size)

            if self.colision_box_pos[0] < 0 and self.colision_box_pos[1] < 0:
                self.new_size = ((self.colision_box_size[0] + self.size[0]) - (self.size[0] - self.colision_box_pos[0]), (self.colision_box_size[1] + self.size[1]) - (self.size[1] - self.colision_box_pos[1]))
                self.new_img = pg.Surface(self.new_size)

            self.empty_col_box = pg.Color(0,0,0,0)
            self.colision_box = pg.Surface(col_box_size, flags=pg.SRCALPHA)

            self.colision_box.convert_alpha()

        else:
            self.is_colision, self.col_state = False, False

        

        self.spriteList.append(self)


    def update(self):
        self.rect.topleft = (self.posX, self.posY)

        if self.is_colision:
            if self.show_col == False:
                self.colision_box.fill(self.empty_col_box)
            else:
                if self.colision_box_size < self.size and (self.colision_box_pos[0] > 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] >= 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] > 0 and self.colision_box_pos[1] >= 0):

                    self.img.blit(self.colision_box, self.colision_box.get_rect())
                    pg.draw.rect(self.img, (255, 0, 0), pg.Rect(self.colision_box_pos[0], self.colision_box_pos[1], self.colision_box_size[0], self.colision_box_size[1]), 1)
                    
                elif self.colision_box_size > self.size and (self.colision_box_pos[0] > 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] >= 0 and self.colision_box_pos[1] > 0 or self.colision_box_pos[0] > 0 and self.colision_box_pos[1] >= 0):
                    self.new_img.blit(self.img, (0, 0))
                    pg.draw.rect(self.new_img, (255, 0, 0), pg.Rect(self.colision_box_pos[0], self.colision_box_pos[1], self.colision_box_size[0], self.colision_box_size[1]), 1)
                    self.new_img.convert_alpha()
                    self.img = self.new_img

                if self.colision_box_pos == (0, 0):
                    self.img.blit(self.colision_box, self.colision_box.get_rect())
                    pg.draw.rect(self.colision_box, (255, 0, 0), pg.Rect(self.colision_box_pos[0], self.colision_box_pos[1], self.colision_box_size[0], self.colision_box_size[1]), 1)
                    

    def get_sprite_size(self):
        return (self.rect[2], self.rect[3])

    def import_image(self, img_path):
        return pg.image.load(img_path).convert_alpha()
