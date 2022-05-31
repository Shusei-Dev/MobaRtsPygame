import pygame as pg
import math


class PlayerClass:

	def __init__(self, gameObj, img, pos, state, prio, id):

		self.gameObj = gameObj
		self.img = img
		self.pos = pos
		self.state = state
		self.prio = prio
		self.id = id

		self.player_entity = self.gameObj.world.entityClass.newEntity("Player", self.img, self.pos, "player", self.prio, self.state, id, 4, 4, 100, (28, 48), (0, 0))

		self.move_x, self.move_y = 0, 0
		self.dis_x, self.dis_y = 0, 0

		self.spriteObj = self.player_entity.spriteObj
		self.spriteObj.show_col = True

		self.basic_dmg = 25
		self.basic_armor = 22
		self.basic_healt = self.player_entity.health
		self.basic_energy = 760
		self.range_radius = 200

		self.camera_centred = None



	def update(self, gameObj):
		self.gameObj = gameObj
		self.input = self.gameObj.input

		self.dt = self.gameObj.renderer.dt

		self.sprite_touch = self.return_sprType_cursor_touch()

		if self.input.mouse_right:

			if self.sprite_touch != None:
				if self.sprite_touch.type == "tile":

					if self.spriteObj.posX < self.input.mouse_pos_clicked[0]:
						self.player_entity.direction = (1, self.player_entity.direction[1])

					if self.spriteObj.posX > self.input.mouse_pos_clicked[0]:
						self.player_entity.direction = (-1, self.player_entity.direction[1])

					if self.spriteObj.posY < self.input.mouse_pos_clicked[1]:
						self.player_entity.direction = (self.player_entity.direction[0], 1)

					if self.spriteObj.posY > self.input.mouse_pos_clicked[1]:
						self.player_entity.direction = (self.player_entity.direction[0], -1)


					self.move_x, self.move_y = self.go_to_cursor()


		if self.sprite_touch != None:
			if self.sprite_touch.type == "entity":
				d = math.sqrt((self.input.mouse_pos_clicked[0] - (self.spriteObj.posX + self.spriteObj.size[0] / 2)) ** 2 + (self.input.mouse_pos_clicked[1] - (self.spriteObj.posY + self.spriteObj.size[1] / 2)) ** 2)
				if d**2 < self.range_radius ** 2:
					self.player_entity.direction = (0, 0)
					self.move_x, self.move_y = 0, 0

					if self.input.mouse_right:
						self.entity_touch = self.get_entity_with_sprite(self.sprite_touch)

						self.entity_touch.looseHp(10, (self.entity_touch, self.entity_touch.hpBarObj))
				else:

					if self.spriteObj.posX < self.input.mouse_pos_clicked[0]:
						self.player_entity.direction = (1, self.player_entity.direction[1])

					if self.spriteObj.posX > self.input.mouse_pos_clicked[0]:
						self.player_entity.direction = (-1, self.player_entity.direction[1])

					if self.spriteObj.posY < self.input.mouse_pos_clicked[1]:
						self.player_entity.direction = (self.player_entity.direction[0], 1)

					if self.spriteObj.posY > self.input.mouse_pos_clicked[1]:
						self.player_entity.direction = (self.player_entity.direction[0], -1)


					self.move_x, self.move_y = self.go_to_cursor()


		self.dis_x = int(abs(self.input.mouse_pos_clicked[0] - self.spriteObj.posX))
		self.dis_y = int(abs(self.input.mouse_pos_clicked[1] - self.spriteObj.posY))

		if self.dis_x <= 2 and self.dis_y <= 2:
			self.move_x, self.move_y = 0, 0
			self.player_entity.direction = (0, 0)


		if self.input.get("y"):
			if self.gameObj.world.cameraClass.centered_on != None and self.camera_centred == True:
				self.gameObj.world.cameraClass.centered_on = None

			if self.gameObj.world.cameraClass.centered_on == None and self.camera_centred == False:
				self.gameObj.world.cameraClass.centered_on = self.player_entity

		if self.input.get("y") == False:
			if self.gameObj.world.cameraClass.centered_on == None:
				self.camera_centred = False
			else:
				self.camera_centred = True

		if not self.spriteObj.sprite_coll_with(self.player_entity.direction, self.player_entity.speed):
			self.spriteObj.posX += self.move_x
			self.spriteObj.posY += self.move_y


	def go_to_cursor(self):
		self.dx = self.input.mouse_pos_clicked[0] - self.spriteObj.posX
		self.dy = self.input.mouse_pos_clicked[1] - self.spriteObj.posY
		self.dist = math.hypot(self.dx, self.dy)
		if self.dist > 0:
			move_x = min(self.player_entity.speed, self.dist) * self.dx / self.dist
			move_y = min(self.player_entity.speed, self.dist) * self.dy / self.dist
			return move_x, move_y
		return 0, 0

	def return_sprType_cursor_touch(self):
		sprite_touch = None
		for all_sprite in self.gameObj.world.spriteClass.spriteList:
			if self.input.mouse_pos_clicked[0] > all_sprite.posX and self.input.mouse_pos_clicked[0] < all_sprite.posX + all_sprite.size[0] and self.input.mouse_pos_clicked[1] > all_sprite.posY and self.input.mouse_pos_clicked[1] < all_sprite.posY + all_sprite.size[1]:
				if sprite_touch == None:
					sprite_touch = all_sprite
				else:
					if all_sprite.priority > sprite_touch.priority:
						sprite_touch = all_sprite
		if sprite_touch != None:
			return sprite_touch


	def get_entity_with_sprite(self, sprite):
		for entity in self.gameObj.world.entityClass.entityList:
			if entity.spriteObj == sprite:
				return entity
