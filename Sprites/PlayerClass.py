import pygame as pg


class PlayerClass:

	def __init__(self, gameObj, img, pos, state, prio, id):

		self.gameObj = gameObj
		self.img = img
		self.pos = pos
		self.state = state
		self.prio = prio
		self.id = id

		

		self.player_entity = self.gameObj.world.entityClass.newEntity("Player", self.img, self.pos, "player", self.state, self.prio, id, 4, 4, 50, (28, 48), (0, 0))
		self.spriteObj = self.player_entity.spriteObj
		self.spriteObj.show_col = False

	def update(self, gameObj):
		self.gameObj = gameObj
		self.input = self.gameObj.input

		self.dt = self.gameObj.renderer.dt

		if self.input

		if self.input.get("z"):
			self.player_entity.direction = (self.player_entity.direction[0], -1)
			if self.spriteObj.sprite_coll_with(self.player_entity.direction, self.player_entity.speed):
				self.player_entity.direction = (self.player_entity.direction[0], 0)

		if self.input.get("s"):
			self.player_entity.direction = (self.player_entity.direction[0], 1)
			if self.spriteObj.sprite_coll_with(self.player_entity.direction, self.player_entity.speed):
				self.player_entity.direction = (self.player_entity.direction[0], 0)

		if self.input.get("z") == False and self.input.get("s") == False:
			self.player_entity.direction = (self.player_entity.direction[0], 0)
		
		if self.input.get("q"):
			self.player_entity.direction = (-1, self.player_entity.direction[1])
			if self.spriteObj.sprite_coll_with(self.player_entity.direction, self.player_entity.speed):
				self.player_entity.direction = (0, self.player_entity.direction[1])

		if self.input.get("d"):
			self.player_entity.direction = (1, self.player_entity.direction[1])
			if self.spriteObj.sprite_coll_with(self.player_entity.direction, self.player_entity.speed):
				self.player_entity.direction = (0, self.player_entity.direction[1])

		if self.input.get("q") == False and self.input.get("d") == False:
			self.player_entity.direction = (0, self.player_entity.direction[1])
	
		self.spriteObj.posX += self.player_entity.speed * self.player_entity.direction[0]
		self.spriteObj.posY += self.player_entity.speed * self.player_entity.direction[1]

