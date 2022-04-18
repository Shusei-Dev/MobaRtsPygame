

class Camera:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.camera_pos = (0, 0)
		self.centered_on = None
		self.is_centered = False

	def center_camera_world(self, world_size, tile_size):
		self.gameSize = self.gameObj.window.game_size
		self.worldSize = (world_size[0] * tile_size, world_size[1] * tile_size)

		self.window_center = (self.gameSize[0] / 2, self.gameSize[1] / 2)
		self.world_center = (self.worldSize[0] / 2, self.worldSize[1] / 2)

		self.mov_x = self.window_center[0] - self.world_center[0]
		self.mov_y = self.window_center[1] - self.world_center[1]

		self.camera_pos = (self.mov_x, self.mov_y)

		for sprites in self.gameObj.world.spriteClass.spriteList:
			sprites.posX += self.mov_x
			sprites.posY += self.mov_y


	def center_camera_target(self, target_pos):
		self.gameSize = self.gameObj.window.game_size
		self.window_center = (self.gameSize[0] / 2, self.gameSize[1] / 2)

		self.mov_x = 0
		self.mov_y = 0

		for sprites in self.gameObj.world.spriteClass.spriteList:
			sprites.posX += self.mov_x
			sprites.posY += self.mov_y


	def move_camera(self, posX, posY):
		self.camera_pos = (self.camera_pos[0] + posX, self.camera_pos[1] + posY)

		for sprites in self.gameObj.world.spriteClass.spriteList:
			sprites.posX += posX
			sprites.posY += posY


	def update(self, gameObj):
		self.gameObj = gameObj

		self.input = self.gameObj.input
		old_mov = (0, 0)

		if self.input.get("up"):
			self.move_camera(0, 4)

		if self.input.get("down"):
			self.move_camera(0, -4)

		if self.input.get("left"):
			self.move_camera(-4, 0)

		if self.input.get("right"):
			self.move_camera(4, 0)

		if self.centered_on != None and self.is_centered == False:
			print("AAA")
			self.center_camera_target((self.centered_on.spriteObj.posX, self.centered_on.spriteObj.posY))
			self.is_centered = True