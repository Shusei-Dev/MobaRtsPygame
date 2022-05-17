
class BasementClass:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.basementType = ["base"]
		self.basementList = []

	def newBasement(self, name, img, pos, basement_type, prio, state, id, health, armor, team, col_box_size=None, col_box_pos=None):
		self.basementSprite = newBasement(self, name, img, pos, basement_type, prio, state, id, health, armor, team, col_box_size, col_box_pos)
		self.basementList.append(self.basementSprite)
		return self.basementSprite

	def update(self, gameObj):
		self.gameObj = gameObj



class newBasement:

	def __init__(self, basementClass, name, img, pos, basement_type, prio, state, id, health, armor, team, col_box_size=None, col_box_pos=None):
		self.basementClass = basementClass
		self.gameObj = self.basementClass.gameObj
		self.entityClass = self.gameObj.world.entityClass
		self.basementType = self.basementClass.basementType

		self.health = health
		self.actual_health = health
		self.armor = armor
		self.team = team

		if basement_type in self.basementType:
			self.type = basement_type
			self.entityObj = self.entityClass.newEntity(name, img, pos, "basement", prio, state, id, 0, 0, self.health, col_box_size, col_box_pos)
			self.spriteObj = self.entityObj.spriteObj

	def update(self):
		self.health = self.entityObj.health
		self.actual_health = self.entityObj.actual_health
		self.spriteObj.update()

