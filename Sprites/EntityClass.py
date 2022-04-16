

class EntityClass:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.entityType = ["player", "monster", "minion"]
		self.entityList = []

	def newEntity(self, name, img, pos, type, prio, state, velocity, health, col_box_size=None, col_box_pos=None):

		self.entityObj = Entity(self.gameObj, self, name, img, pos, type, prio, state, velocity, health, col_box_size, col_box_pos)
		self.entityList.append(self.entityObj)
		return self.entityObj

	def update(self, gameObj):
		self.gameObj = gameObj

class Entity:

	def __init__(self, gameObj,  entityClass, name, img, pos, type, prio, state, velocity, health, col_box_size, col_box_pos):

		self.spriteClass = gameObj.world.spriteClass
		self.entityType = entityClass.entityType

		self.velocity = velocity
		self.health = health

		if type in self.entityType:
			self.spriteObj = self.spriteClass.newSprite(name, img, pos, type, prio, state, col_box_size=col_box_size, col_box_pos=col_box_pos)

	def update(self, gameObj):
		self.gameObj = gameObj
		self.spriteObj.update()
