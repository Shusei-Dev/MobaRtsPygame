import pygame as pg

class EntityClass:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.entityType = ["player", "monster", "minion", "basement"]
		self.entityList = []

	def newEntity(self, name, img, pos, type, prio, state, id, velocity, speed, health, col_box_size=None, col_box_pos=None):

		self.entityObj = Entity(self, name, img, pos, type, prio, state, id, velocity, speed, health, col_box_size, col_box_pos)
		self.entityList.append(self.entityObj)
		if self.entityObj.hpBarObj != None:
			self.entityList.append(self.entityObj.hpBarObj)
		return self.entityObj

	def update(self, gameObj):
		self.gameObj = gameObj
		self.entityObj.update_entityClass(self)

class Entity:

	def __init__(self, entityClass, name, img, pos, type, prio, state, id, velocity, speed, health, col_box_size, col_box_pos):

		self.entityClass = entityClass
		self.gameObj = self.entityClass.gameObj
		self.spriteClass = self.gameObj.world.spriteClass
		self.entityType = self.entityClass.entityType

		self.velocity = velocity
		self.direction = (0, 0)
		self.speed = speed
		self.health = health
		self.actual_health = health
		self.isMoving = False

		if type in self.entityType:
			self.type = type
			self.spriteObj = self.spriteClass.newSprite(name, img, pos, "entity", prio, state, id, col_box_size=col_box_size, col_box_pos=col_box_pos)

		self.hpBarObj = HpBar(self.health, self.spriteClass, name, pos, self.spriteObj.size, 5, state, id)

		self.update()
		
	def update_entityClass(self, entityClass):
		self.entityClass = entityClass

	def update(self):

		self.entityList = self.entityClass.entityList
		
		self.spriteObj.update()
		self.hpBarObj.getSpritePos(self.spriteObj.posX, self.spriteObj.posY)
		self.isEntityMoving()

	def isEntityMoving(self):
		if self.direction != (0, 0):
			self.isMoving = True

	def looseHp(self, hp, entity_target):
		entity_actual_hp = 0
		
		for entity in self.entityList:
			if entity.spriteObj.type != "hpBar" and entity.spriteObj.spr_id == entity_target[0].spriteObj.spr_id:
				entity.actual_health -= hp
				entity_actual_hp = entity.actual_health
			else:
				print(entity.type)
				entity_target[1].changeHpBar(entity_actual_hp)

	def regenHp(self, hp, entity_target):
		entity_actual_hp = 0
		for entity in self.entityList:
			if entity.spriteObj.type != "hpBar" and entity.spriteObj.spr_id == entity_target[0].spriteObj.spr_id:
				entity.actual_health += hp
				entity_actual_hp = entity.actual_health
			else:
				entity.changeHpBar(entity_actual_hp)


class HpBar:

	def __init__(self, health, spriteClass, name, pos, size, prio, state, id):
		
		self.hpBarMaxLen = 100

		self.health = health
		self.spriteSize = size
		self.type = "hpBar"
		self.spriteClass = spriteClass

		
		self.hpBarSize = (100, 12)
		self.hpBarSurface = pg.Surface(self.hpBarSize)
		self.hpBarSurface.fill((0, 255, 0))
		self.spriteObj = self.spriteClass.newSprite(name + "hpBar", self.hpBarSurface, (pos[0] - (self.hpBarSize[0] / 2) + (self.spriteSize[0] / 2), pos[1] - 20), "hpBar", prio, state, id)

	def getSpritePos(self, posX, posY):
		self.spritePos = (posX, posY)

	def change_max_hp(self, new_hp):
		self.health = new_hp

	def changeHpBar(self, hp):
		self.new_hpBar_size = (hp * self.hpBarMaxLen) / self.health
		self.hpBarSurface.fill((0, 0, 0))
		self.hpRect = pg.Rect(0, 0, self.new_hpBar_size, self.hpBarSize[1])
		pg.draw.rect(self.hpBarSurface, (0, 255, 0), self.hpRect)
		self.spriteObj.img = self.hpBarSurface
		self.spriteObj.update()
		

	def update(self):
		self.spriteObj.posX = self.spritePos[0] - (self.hpBarSize[0] / 2) + (self.spriteSize[0] / 2)
		self.spriteObj.posY = self.spritePos[1] - 20

		self.spriteObj.update()

