

class EntityClass:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.entityType = ["player", "monster", "minion"]
		self.entityList = []

	def newEntity(self, name, img, pos, type, prio, state, id, velocity, speed, health, col_box_size=None, col_box_pos=None):

		self.entityObj = Entity(self, name, img, pos, type, prio, state, id, velocity, speed, health, col_box_size, col_box_pos)
		self.entityList.append(self.entityObj)
		return self.entityObj

	def update(self, gameObj):
		self.gameObj = gameObj

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
		self.isMoving = False

		if type in self.entityType:
			self.type = type
			self.spriteObj = self.spriteClass.newSprite(name, img, pos, type, prio, state, id, col_box_size=col_box_size, col_box_pos=col_box_pos)

	def update(self):
		
		self.spriteObj.update()
		self.isEntityMoving()

	def isEntityMoving(self):
		if self.direction != (0, 0):
			self.isMoving = True

