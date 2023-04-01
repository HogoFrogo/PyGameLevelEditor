#region Imports
import pygame
import button
import csv
import pickle
#endregion

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#region game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 360

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')
#endregion


#define game variables
ROWS = 11
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 43
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
tile_heights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# tile_heights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2]

#load images
bg_img_2 = pygame.image.load('img/Background/bg_img_2.png').convert_alpha()
bg_img_3 = pygame.image.load('img/Background/bg_img_3.png').convert_alpha()
bg_img_1 = pygame.image.load('img/Background/bg_img_1.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile2/{x}.png').convert_alpha()
	img_height = tile_heights[x]
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE*img_height))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 20)

#create empty tile list
world_data = []
for row in range(ROWS):
	cell_row = []
	for col in range(MAX_COLS):
		cell = [-1,-1,-1,-1]
		cell_row.append(cell)
	world_data.append(cell_row)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = [-1,-1,-1,-1]


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#create function for drawing background
def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(bg_img_1, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - bg_img_1.get_height() - 300))
		screen.blit(bg_img_2, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - bg_img_2.get_height() - 150))
		screen.blit(bg_img_3, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - bg_img_3.get_height()))

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tiles in enumerate(row):
			#print(tiles)
			for z, tile in enumerate(tiles):
				if tile >= 0:
					#print(tile)
					img_height = tile_heights[tile]
					screen.blit(img_list[tile], (x * TILE_SIZE - scroll, (y-(img_height-1)) * TILE_SIZE))



#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	cell_size=55
	button_list_margin=15
	tile_button = button.Button(SCREEN_WIDTH + (cell_size * button_col) + button_list_margin, cell_size * button_row + button_list_margin, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 4:
		button_row += 1
		button_col = 0


run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text('UP/DOWN - change level, LEFT/RIGHT - scroll, +Shift - speed', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 65)
	draw_text(f'Editor for HogoFrogo', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 40)

	#region save and load data
	if save_button.draw(screen):
		#save level data
		with open(f'level_files/level_{level}_terrain.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[1]
					numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
					if element not in numbers:
						element = -1
					new_row.append(element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_bg_palms.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[0]
					new_element = -1
					numbers = [16]
					if element in numbers:
						new_element = element - 16
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_fg_palms.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[2]
					new_element = -1
					numbers = [17,18]
					if element in numbers:
						new_element = element - 17
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_houses.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[0]
					new_element = -1
					numbers = [19,20,21,22] #4
					if element in numbers:
						new_element = element - 19
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_crates.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[1]
					new_element = -1
					numbers = [23]
					if element in numbers:
						new_element = element - 23
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_enemies.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[1]
					new_element = -1
					numbers = [24,25,26,27,28,29]
					if element in numbers:
						new_element = element - 24
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_coins.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[1]
					new_element = -1
					numbers = [30,31]
					if element in numbers:
						new_element = element - 30
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_grass.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[0]
					new_element = -1
					numbers = [32,33,34,35,36]
					if element in numbers:
						new_element = element - 32
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_player.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[1]
					new_element = -1
					numbers = [37,38]
					if element in numbers:
						new_element = element - 37
					new_row.append(new_element)
				writer.writerow(new_row)
		with open(f'level_files/level_{level}_constraints.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				new_row =[]
				for tiles in row:
					element = tiles[3]
					new_element = -1
					numbers = [39,40,41,42]
					if element in numbers:
						new_element = element - 39
					new_row.append(new_element)
				writer.writerow(new_row)
		#soundeffect
		save_sound = pygame.mixer.Sound('save.wav')
		save_sound.play(0)
#endregion

		#alternative pickle method
		#pickle_out = open(f'level{level}_data', 'wb')
		#pickle.dump(world_data, pickle_out)
		#pickle_out.close()

	if load_button.draw(screen):
		world_data = []
		for row in range(ROWS):
			cell_row = []
			for col in range(MAX_COLS):
				cell = [-1,-1,-1,-1]
				cell_row.append(cell)
			world_data.append(cell_row)


#region load in level data
		#reset scroll back to the start of the level
		scroll = 0

		with open(f'level_files/level_{level}_grass.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][0] = int(tile)+32 ###
		with open(f'level_files/level_{level}_terrain.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][1] = int(tile)
		with open(f'level_files/level_{level}_bg_palms.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][0] = int(tile)+16
		with open(f'level_files/level_{level}_fg_palms.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][2] = int(tile)+17
		with open(f'level_files/level_{level}_houses.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][0] = int(tile)+19
		with open(f'level_files/level_{level}_crates.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][1] = int(tile)+23
		with open(f'level_files/level_{level}_enemies.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][1] = int(tile)+24
		with open(f'level_files/level_{level}_coins.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][1] = int(tile)+30
		with open(f'level_files/level_{level}_player.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][1] = int(tile)+37
		with open(f'level_files/level_{level}_constraints.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					if(int(tile)>-1):
						world_data[x][y][3] = int(tile)+39
#endregion
		#alternative pickle method
		#world_data = []
		#pickle_in = open(f'level{level}_data', 'rb')
		#world_data = pickle.load(pickle_in)				

	#draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE
	if(y>10):
		y=10

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		layer = 1
		if(current_tile in [16,32,33,34,35,36,19,20,21,22]): # bg palms and grass and houses
			layer = 0
		if(current_tile in [17,18]): # fg palms
			layer = 2
		if(current_tile in [39,40,41,42]): # constraints
			layer = 3
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x][layer] != current_tile:
				world_data[y][x][layer] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = [-1,-1,-1,-1]


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()

