

class Camera:

	def __init__(self, gameObj):
		self.gameObj = gameObj

		self.camera_pos = (0, 0)
		self.centered_on = None
		self.is_centered = False

		self.move_speed_cam = 8

	def center_camera_world(self, world_size, tile_size):
		self.gameSize = self.gameObj.window.game_size
		self.worldSize = (world_size[0] * tile_size, world_size[1] * tile_size)

		self.window_center = (self.gameSize[0] / 2, self.gameSize[1] / 2)
		self.world_center = (self.worldSize[0] / 2, self.worldSize[1] / 2)

		self.mov_x = self.window_center[0] - self.world_center[0]
		self.mov_y = self.window_center[1] - self.world_center[1]

		self.camera_pos = (self.mov_x, self.mov_y)

		for sprites in self.gameObj.world.spriteClass.spriteList:
			if sprites.isNotMoveble == False:
				sprites.posX += self.mov_x
				sprites.posY += self.mov_y


	def center_camera_target(self, target):
		self.gameSize = self.gameObj.window.game_size
		self.target = target

		self.window_center = (self.gameSize[0] / 2, self.gameSize[1] / 2)

		self.target_center = self.target.posX + self.target.size[0] / 2, self.target.posY + self.target.size[1] / 2

		self.center_move = (self.window_center[0] - self.target_center[0], self.window_center[1] - self.target_center[1])

		for sprites in self.gameObj.world.spriteClass.spriteList:

			sprites.posX += self.center_move[0]
			sprites.posY += self.center_move[1]


	def move_camera(self, posX, posY):
		self.camera_pos = (self.camera_pos[0] + posX, self.camera_pos[1] + posY)

		for sprites in self.gameObj.world.spriteClass.spriteList:
			if not sprites.isNotMoveble:
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

		if self.centered_on == None and self.is_centered == False:
			if self.input.mouse_pos[1] < 50:
				self.move_camera(0, self.move_speed_cam)

			if self.input.mouse_pos[1] > self.gameObj.window.game_size[1] - 50:
				self.move_camera(0, -self.move_speed_cam)

			if self.input.mouse_pos[0] < 50:
				self.move_camera(self.move_speed_cam, 0)

			if self.input.mouse_pos[0] > self.gameObj.window.game_size[0] - 50:
				self.move_camera(-self.move_speed_cam, 0)


		if self.centered_on != None and self.centered_on.isMoving:
			self.is_centered = False

		if self.centered_on != None and self.is_centered == False:
			self.center_camera_target(self.centered_on.spriteObj)
			self.is_centered = True
