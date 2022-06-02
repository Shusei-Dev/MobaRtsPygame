from Sprites.CreepClass import *
import math

class BasementClass:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.basementType = ["base"]
		self.basementClassByType = {"base": newBase}
		self.basementList = []

		self.creepClass = CreepClass(self.gameObj)

	def newBasement(self, name, img, pos, basement_type, prio, state, id, health, damage, armor, team, col_box_size=None, col_box_pos=None):
		self.basementEntity = self.basementClassByType[basement_type](self, self.creepClass, name, img, pos, "minion", prio, state, id, health, armor, team, col_box_size, col_box_pos)
		self.basementList.append(self.basementEntity)
		return self.basementEntity

	def update(self, gameObj):
		self.gameObj = gameObj
		self.gameObj.world.addSpritestoList(self.creepClass.creepsList)
		self.creepClass.update(self.gameObj)

		for basement_entity in self.basementList:
			basement_entity.update_Class(self)



class newBase:

	def __init__(self, basementClass, creepClass, name, img, pos, type, prio, state, id, health, armor, team, col_box_size=None, col_box_pos=None):
		self.basementClass = basementClass
		self.gameObj = self.basementClass.gameObj
		self.entityClass = self.gameObj.world.entityClass
		self.basementType = self.basementClass.basementType

		self.creepClass = creepClass

		self.health = health
		self.actual_health = health
		self.armor = armor
		self.team = team

		self.type = type
		self.entityObj = self.entityClass.newEntity(name, img, pos, self.type, prio, state, id, 0, 0, self.health, col_box_size, col_box_pos)
		self.spriteObj = self.entityObj.spriteObj

	def update_Class(self, basementClass):
		self.basementClass = basementClass


	def update(self):
		self.entityObj.update()

		self.health = self.entityObj.health
		self.actual_health = self.entityObj.actual_health
		self.gameObj = self.basementClass.gameObj
		self.gameTime = self.gameObj.world.gameTime

		if self.gameTime["minutes"] == 0 and round(self.gameTime["seconds"]) == 5:
			self.creepClass.newCreep("test", "res/entity/minion_test.png", (self.spriteObj.posX + (self.spriteObj.size[0] / 2) - 5, self.spriteObj.posY - (self.spriteObj.size[1] / 2)), "soldier", 3, True, "#2", 30, 10, 0, 25, "blue")
