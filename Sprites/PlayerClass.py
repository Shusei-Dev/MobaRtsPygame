
class PlayerClass:

	def __init__(self, gameObj, img, pos, state, prio):

		self.gameObj = gameObj
		self.img = img
		self.pos = pos
		self.state = state
		self.prio = prio

		self.player_entity = self.gameObj.world.entityClass.newEntity("Player", self.img, self.pos, "player", self.state, self.prio, 10, 50, (28, 46), (0, 0))
		self.spriteObj = self.player_entity.spriteObj

	def update(self, gameObj):
		self.gameObj = gameObj
		self.input = self.gameObj.input

		self.dt = self.gameObj.renderer.dt

		if self.input.get("z"):
			self.spriteObj.posY -= self.player_entity.velocity 
		if self.input.get("s"):
			self.spriteObj.posY += self.player_entity.velocity 
		if self.input.get("q"):
			self.spriteObj.posX -= self.player_entity.velocity 
		if self.input.get("d"):
			self.spriteObj.posX += self.player_entity.velocity