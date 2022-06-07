from PIL import Image


def get_pixel(self, img, pos, size):
	rgb_img = img.convert('RGB')
	if pos[0] + 1 <= size[0] and pos[1] + 1 <= size[1]:
		r, g, b = rgb_img.getpixel(pos)
		return (r, g, b)

def import_spriteSheet(self, img, sprite_table, nmb_id):
	self.original_path = os.getcwd()
	self.img_path = self.original_path + "/res/SpriteSheets"

	self.img = Image.open(self.img_path + "/" + img)
	spritesheet_name = img

	sprites_list = []
	scanning = False
	old_x, old_y = 0, 0
	nmb_sprite = 0
	origine = (0, 0)
	sprite_check = False
	sprite_found = False
	size = self.img.size
	sprite_data = {"pixels": [], "size": (0, 0), "id": "", "name": "none"}
	x, y = -1, 0
	old_origine = (0, 0)
	id_sprite = ""
	self.nmb_id = nmb_id

	red, blue, yellow = (255, 0, 0), (0, 0, 255), (255, 255, 0)

	while True:
		if sprite_found and sprite_data != {"pixels": [], "size": (0, 0), "id": "", "name": "none"}:
			if not sprite_check:
				
				if x >= origine[0] + sprite_data["size"][0] + 1:
					y += 1
					x = origine[0] + 1
				
				else:
					if scanning:
						sprite_data["pixels"].append(self.get_pixel(self.img, (x, y), size))
					x += 1

				if x >= size[0] and y >= size[1]:
					print(f"The spritesheet {spritesheet_name} has been loaded")
					return sprites_list

			if y >= sprite_data["size"][1] + old_origine[1] and x >= old_origine[0] + sprite_data["size"][0] and sprite_check:
				sprite_data["id"] = "#" + str(self.nmb_id)
				for k in sprite_table:
					if sprite_table[k] == sprite_data["id"]:
						sprite_data["name"] = k
						#print(sprite_data["name"], sprite_data["id"])
				sprites_list.append(sprite_data)
				nmb_sprite += 1
				self.nmb_id += 1 
				old_x, old_y = x, y
				x, y = origine[0], origine[1]
				sprite_found, sprite_check = False, False
				sprite_data = {"pixels": [], "size": (0, 0), "id": "", "name": "none"}	

		else:
			if x >= size[0]:
				y += 1
				x = origine[0]
			else:
				x += 1

			if old_x >= size[0] - 2 and old_y >= size[1] - 1:
				print(f"The spritesheet {spritesheet_name} has been loaded")
				return sprites_list
				
			if x >= size[0] and y >= size[1]:
				print(f"The spritesheet {spritesheet_name} has been loaded")
				return sprites_list
		
		pix = self.get_pixel(self.img, (x, y), size)
		
		if pix == red:
			if self.get_pixel(self.img, (x+1, y), size) == yellow:
				if sprite_found == False:
					sprite_found = True
				else:
					sprite_data["size"] = (x - origine[0] - 2, y)
					scanning = True

		if y - 1 > 0 and self.get_pixel(self.img, (x, y - 1), size) == blue and sprite_found:
			sprite_data["size"] = (x - origine[0], y - origine[1])
			
			x = origine[0] + 1
			y = origine[1] + 1
			scanning = True
			

		if sprite_found == True and pix == blue and sprite_data["size"] == (0, 0) and self.get_pixel(self.img, (x, y-1), size) == red:
			sprite_data["size"] = (size[0] - origine[0] - 2, y)
			x = origine[0] + 1
			y = origine[1] + 1
			scanning = True


		if pix == yellow and self.get_pixel(self.img, (x - 1, y), size) != red and sprite_data["size"] == (0, 0):
			if sprite_found:
				sprite_data["size"] = (x - origine[0] - 1, y)

		
		if pix == yellow and self.get_pixel(self.img, (x - 1, y), size) != red and sprite_found:
			
			scanning = False

		if pix == blue and self.get_pixel(self.img, (x + 1, y), size) == red and sprite_found:
			sprite_data["size"] = (sprite_data["size"][0], y - origine[1] - 1)
			if not sprite_check:
				old_origine = origine
				if x + 1 >= size[0] - 1:
					origine = (0, y + 1)
				else:
					origine = (old_origine[0] + sprite_data["size"][0] + 2, origine[1])

				sprite_check = True

		if spritesheet_name != "sprite_sheet.png":
			#print(x, y, scanning, sprite_data["size"])
			pass