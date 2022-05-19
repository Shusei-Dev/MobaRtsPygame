import pygame as pg
from Sprites.SpriteClass import *
from Sprites.EntityClass import *
from Sprites.PlayerClass import *
from Sprites.TileClass import *
from Sprites.BasementClass import *
from Sprites.CreepClass import *
from FontSystem import *
from camera import *
import random, json, sys

class World:

    def __init__(self, gameObj):

        self.gameObj = gameObj


        # --Initialize all the class--
        self.spriteClass = Sprite(self.gameObj)
        self.tileClass = TileClass(self.gameObj)
        self.entityClass = EntityClass(self.gameObj)
        self.creepClass = CreepClass(self.gameObj)
        self.basementClass = BasementClass(self.gameObj)

        self.cameraClass = Camera(self.gameObj)
        self.fontClass = FontClass(self.gameObj)

        self.worldSprites = []

        self.assets = self.gameObj.assets

        with open("Sprites/sprite_table.json", "r") as sprite_table:
            self.sprite_id_table = json.load(sprite_table)


    def search_id_in_table(self, spr_id, spr_type):
        for sprite_type in self.sprite_id_table:
            if sprite_type == spr_type:
                for sprite_id in self.sprite_id_table[sprite_type]:
                    if sprite_id == spr_id:
                        return self.sprite_id_table[sprite_type][sprite_id]

    def create_tile_with_id(self, id, pos):

        self.tile_info = self.search_id_in_table(id, "tile")
        if self.tile_info["type"] == "background":
            return self.tileClass.newTile(self.tile_info["name"], self.tile_info["img"], pos, self.tile_info["type"], self.tile_info["prio"], True, id)
        else:
            return self.tileClass.newTile(self.tile_info["name"], self.tile_info["img"], pos, self.tile_info["type"], self.tile_info["prio"], True, id, (self.tile_info["col_size"][0], self.tile_info["col_size"][1]) , (self.tile_info["col_pos"][0], self.tile_info["col_pos"][1]))

    def get_id_with_table(self, nmb, table):
        for e in table:
            if table[e] == nmb:
                return e

    def addSpritestoList(self, spriteList):
        for sprite in spriteList:
            if sprite not in self.worldSprites:
                self.worldSprites.append(sprite)

    def check_size_world(self):
        x_tile_len = 0

        for x_tile in self.tile_map:
            if len(x_tile) > x_tile_len:
                x_tile_len = len(x_tile)


        if x_tile_len == self.world_size["width"] and len(self.tile_map) == self.world_size["height"]:
            return True
        else:
            return False

    def init_world(self, world_path):
        # -- Load json world map --
        self.world_path = world_path
        with open(self.world_path, "r") as read_file:
            self.world_file = json.load(read_file)

        self.world_size = self.world_file["map_size"]
        self.id_table = self.world_file["tiles_ids_table"]
        self.tile_map = self.world_file["tile_map"]
        self.entity_pos = self.world_file["entitys_pos"]
        self.tile_size = (self.world_file["tiles_size"]["width"], self.world_file["tiles_size"]["height"])
        self.entitys_pos = self.world_file["entitys_pos"]
        self.colision_map = self.world_file["colision_map"]

        self.world_map = {"tile": [], "entity": []}
        self.show_world_col = False

        if not self.check_size_world():
            print("The size of the world is wrong ! Check the map json file")
            sys.exit()

        tile_y = 0
        for y in self.tile_map:
            tile_x = 0
            self.world_map["tile"].append([])
            for x in self.tile_map[self.tile_map.index(y)]:

                self.world_map["tile"][tile_y].append(self.create_tile_with_id(self.get_id_with_table(x, self.id_table), (self.tile_size[0] * tile_x, self.tile_size[1] * tile_y)))
                tile_x += 1
            tile_y += 1

        tile_y = -1
        for y in range(-1, len(self.colision_map)):
            tile_x = 0
            for x in range(len(self.colision_map[y])):
                if self.colision_map[y][x] == 1:
                    set_col_tile = self.world_map["tile"][y][x]
                    del self.tileClass.tileList[self.tileClass.tileList.index(set_col_tile)]
                    set_col_tile.set_state_col(True, self.show_world_col)
                    self.tileClass.tileList.append(set_col_tile)
                else:
                    set_col_tile = self.world_map["tile"][y][x]
                    del self.tileClass.tileList[self.tileClass.tileList.index(set_col_tile)]
                    set_col_tile.set_state_col(False, False)
                    self.tileClass.tileList.append(set_col_tile)
                tile_x += 1
            tile_y += 1

        for entitys in self.entitys_pos:
            entity = self.search_id_in_table(entitys, "entity")
            if entity["type"] == "player":
                entity_pos = (self.entitys_pos[entitys][0][0], self.entitys_pos[entitys][0][1])
                self.player = PlayerClass(self.gameObj, entity["img"], entity_pos, True, 2, entitys)

            if entity["type"] == "basement":
                entity_pos = (self.entitys_pos[entitys][0][0], self.entitys_pos[entitys][0][1])
                self.basementClass.newBasement(entity["name"], entity["img"], entity_pos, entity["basement_type"], entity["prio"], True, entitys, entity["health"], entity["damage"], entity["armor"], entity["team"], (entity["col_size"][0], entity["col_size"][1]), (entity["col_pos"][0], entity["col_pos"][1]))


        self.cameraClass.center_camera_world((self.world_size["width"], self.world_size["height"]), self.tile_size[0])



    def update(self, gameObj):
        self.gameObj = gameObj

        self.addSpritestoList(self.tileClass.tileList)
        self.addSpritestoList(self.entityClass.entityList)
        self.addSpritestoList(self.basementClass.basementList)

        self.dt = self.gameObj.renderer.dt

        self.spriteClass.update(self.gameObj)
        self.tileClass.update(self.gameObj)
        self.entityClass.update(self.gameObj)
        self.basementClass.update(self.gameObj)

        self.player.update(self.gameObj)
        self.cameraClass.update(self.gameObj)

        self.prio_sprites = self.spriteClass.prio_sprites

        for sprite in self.worldSprites:
            sprite.update()
