import pygame
import time
import random
import queue

# colors
BLACK =(0 ,0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (243, 250, 100)

PURPLE = (88, 25, 100)
NICE_GREEN = (3, 237, 100)
ORANGE = (244, 135, 100)
OCEAN = WHITE
PINK = WHITE

BEGIN_COLOR = GREEN
FINISH_COLOR = RED
RUN_COLOR = YELLOW
BORDERING_COLOR = BLACK
CLEAR_COLOR = PURPLE
RUBBER_COLOR = NICE_GREEN
RANDOM_COLOR = BLUE

# screen sizes
ACTUAL_WIDTH = 1200
ACTUAL_HEIGHT = 800
WIDTH = 800
HEIGHT = 800

# squar sizes
SQ_X = 20
SQ_Y = 20
SQ_WIDTH = 1
SQ_BORDER_WIDTH = 2
SQ_COLOR = BLACK
SQ_BORDER_COLOR = BLACK

# label
LABEL_SIZE = 50
LABEL_WIDTH = WIDTH + 50
LABEL_GAP = 100
LABEL_STRING_GAP = 100

# font
FONT_NAME = "Roboto-Thin.ttf"
FONT_SIZE = 24
FONT_COLOR = BLACK
CHOSEN_FONT_COLOR = RED

pygame.font.init()
font = pygame.font.Font(FONT_NAME, FONT_SIZE)




# # font
# FONT = pygame.font.SysFont("arialboldttf", 72)
# def get_text(string, color, size):
# 	text = FONT.render(string, True, color)
# 	return text

def absolut(fx, sx):
	if fx < sx:
		return 1
	else:
		return -1


def random_color():
	return (random.randint(0,255), random.randint(0,255), random.randint(0,255))


class Label():
	def __init__(self, id=0, name="", x=0, y=0, size=0, color=BLACK, chosen=False, done=False, screen=None, text_size=30, gap_label_text=20):
		self.id = id
		self.name = name
		self.x = x
		self.y = y
		self.size = size
		self.color = color
		self.chosen = chosen
		self.done = done
		self.screen = screen
		self.text_size = text_size
		self.gap_label_text = gap_label_text
		self.text_x = self.x + LABEL_STRING_GAP
		self.text_y = self.y
		self.text_pos = (self.text_x, self.text_y)
		self.text = font.render(self.name, True, FONT_COLOR)

	def is_chosen(self, x, y):
		if self.x < x < self.x + self.size and self.y < y < self.y + self.size:
			self.chosen = True
			self.text = font.render(self.name, True, CHOSEN_FONT_COLOR)
			return True
		self.text = font.render(self.name, True, FONT_COLOR)
		return False

	def draw(self):
		pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.size, self.size])
		self.screen.blit(self.text, self.text_pos)


class Square():
	def __init__(self, id, x, y, color=SQ_COLOR, border_color=SQ_BORDER_COLOR, taken=False):
		self.id = id
		self.x = x
		self.y = y
		self.color = color
		self.border_color = border_color
		self.taken = False

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, [self.x + SQ_BORDER_WIDTH, self.y+SQ_BORDER_WIDTH, SQ_X-SQ_BORDER_WIDTH,
		 SQ_Y-SQ_BORDER_WIDTH])
		

class Board():
	def __init__(self, screen):
		self.begin = (0,0)
		self.finish = (1,1)

		x_n = int(WIDTH/SQ_X)
		y_n = int(HEIGHT/SQ_Y)
		self.squares = [[None for j in range(x_n)] for i in range(y_n)]

		for i in range(y_n):
			for j in range(x_n):
				x = SQ_X * j
				y = SQ_Y * i
				index = i*x_n + j
				self.squares[i][j] = Square(index, x, y)

		self.screen = screen
		self.x_elements = x_n
		self.y_elements = y_n
	

		# 0 = border
		# 1 = start
		# 2 = finish
		# 3 = run
		# 4 = after_run
		self.status = 0 
		self.label_borders = Label(id=0, name="Borders", x = LABEL_WIDTH, y = 0, size = LABEL_SIZE, screen=self.screen, color = BORDERING_COLOR)
		self.label_begin = Label(id=1, name = "Begin", x = LABEL_WIDTH, y = LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = BEGIN_COLOR)
		self.label_finish = Label(id=2, name = "Finish", x = LABEL_WIDTH, y = 2*LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = FINISH_COLOR)
		self.label_run = Label(id=3, name = "Run", x = LABEL_WIDTH, y = 3*LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = RUN_COLOR)
		self.label_clear = Label(id=5, name = "Clear", x = LABEL_WIDTH, y = 4*LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = CLEAR_COLOR)
		self.label_rubber = Label(id=6, name = "Rubber", x = LABEL_WIDTH, y = 5*LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = RUBBER_COLOR)
		self.label_random = Label(id=7, name = "Radnom", x = LABEL_WIDTH, y = 6*LABEL_GAP, size = LABEL_SIZE, screen=self.screen, color = RANDOM_COLOR)

		self.labels = [self.label_random, self.label_begin, self.label_borders, self.label_finish, self.label_run, self.label_clear, self.label_rubber]


	def is_in_range(self, x, y, pathfinding=False):
		if pathfinding:
			if self.finish == (x,y):
				return True
		if 0 <= x < self.x_elements  and 0 <= y < self.y_elements:
			if not self.squares[y][x].taken:
				return True
		return False

	def display(self):
		self.screen.fill(WHITE)
		for i in range(self.y_elements):
			for j in range(self.x_elements):
				self.squares[i][j].draw(self.screen)
		for label in self.labels:
			label.draw()
		pygame.display.flip()

	def fast_display(self, x, y):
		self.squares[y][x].draw(self.screen)
		pygame.display.flip()

	def setting_borders(self, pos_x, pos_y):
		if pos_x > WIDTH:
			return

		x = int(pos_x // SQ_X)
		y = int(pos_y // SQ_Y)

		self.squares[y][x].color = PINK
		self.squares[y][x].taken = True 


	def setting_begin(self, pos_x, pos_y):
		x = pos_x // SQ_X
		y = pos_y // SQ_Y
		if self.is_in_range(x, y):
			self.squares[self.begin[1]][self.begin[0]].color = BLACK
			self.squares[self.begin[1]][self.begin[0]].taken = False
			self.squares[y][x].taken = True
			self.squares[y][x].color = BEGIN_COLOR
			self.begin = (x, y)


	def setting_finish(self, pos_x, pos_y):
		x = pos_x // SQ_X
		y = pos_y // SQ_Y
		if self.is_in_range(x, y):
			self.squares[self.finish[1]][self.finish[0]].color = BLACK
			self.squares[self.finish[1]][self.finish[0]].taken = False

			self.squares[y][x].taken = True
			self.squares[y][x].color = FINISH_COLOR
			self.finish = (x, y)


	def clear(self):
		for i in range(self.y_elements):
			for j in range(self.x_elements):
					self.squares[i][j].color = SQ_COLOR
					self.squares[i][j].taken = False
		self.squares[self.begin[1]][self.begin[0]].color = BEGIN_COLOR
		self.squares[self.finish[1]][self.finish[0]].color = FINISH_COLOR
		self.squares[self.begin[1]][self.begin[0]].taken = True
		self.squares[self.finish[1]][self.finish[0]].taken = True


		self.display()

	def rubber(self, x, y):
		x = x // SQ_X
		y = y // SQ_Y
		if self.begin == (x, y) or self.finish == (x, y):
			return
		if 0 <= x < self.x_elements and 0 <= y < self.y_elements:
			self.squares[y][x].taken = False
			self.squares[y][x].color = SQ_COLOR
			self.fast_display(x, y)




	def pathfinder(self, start, finish):
		if start == finish or not self.is_in_range(start[1], start[0]):
			return
		else:
			x = start[0]
			y = start[1]
			q = queue.Queue()
			p = []
			q.put([start[0], start[1], p])

			while q.not_empty:
				print(q.qsize())
				if q.qsize() == 0:
					return


				block = q.get()
				x = block[0]
				y = block[1]

				self.squares[y][x].color = NICE_GREEN
				self.squares[y][x].taken = True
				self.fast_display(x, y)

				path = block[2].copy()
				if path is None:
					path = []
				path.append((x,y))


				if x == finish[0] and y == finish[1]:
					for el in path:
						self.squares[el[1]][el[0]].color = RED
						self.display()
						time.sleep(0.01)
					return

				if self.is_in_range(x+1,y, pathfinding=True):
					q.put([x+1,y, path])
					self.squares[y][x+1].taken = True
				if self.is_in_range(x,y+1, pathfinding=True):
					q.put([x,y+1, path])
					self.squares[y+1][x].taken = True
				if self.is_in_range(x-1,y, pathfinding=True):
					q.put([x-1,y, path])
					self.squares[y][x-1].taken = True
				if self.is_in_range(x,y-1, pathfinding=True):
					q.put([x,y-1, path])
					self.squares[y-1][x].taken = True

		return

	def random_borders(self, percent):
		i = (self.x_elements * self.y_elements)*(percent)//100
		for i in range(i):
			x = random.randint(0, self.x_elements-5)
			y = random.randint(0, self.y_elements-5)
			self.squares[y][x].taken = True
			self.squares[y][x].color = PINK

	def label_chosing(self, x, y):
		for label in self.labels:
			if label.is_chosen(x,y):
				if self.status == 4:
					if label.id == 5:
						self.status = 5
				else:
					self.status = label.id


		
def main():
	screen = pygame.display.set_mode((ACTUAL_WIDTH, ACTUAL_HEIGHT))
	pygame.display.set_caption('PATH FINDING')


	pygame.display.flip()
	running = True

	board = Board(screen)
	clean = True


	while running:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            running = False
	        if pygame.mouse.get_pressed()[0]:
	        	x = pygame.mouse.get_pos()[0]
	        	y = pygame.mouse.get_pos()[1]
	        	
	        	board.label_chosing(x, y)

	        	if board.status == 0:
	        		board.setting_borders(x, y)
	        	elif board.status == 1:
	        		board.setting_begin(x, y)
	        	elif board.status == 2:
	        		board.setting_finish(x, y)
	        	elif board.status == 3:
	        		print(board.begin, board.finish)
	        		board.pathfinder(board.begin, board.finish)
	        		board.status = 4
	        	elif board.status == 5:
	        		board.clear()

	        	elif board.status == 6:
	        		board.rubber(x,y)
	        	elif board.status == 7:
	        		board.random_borders(20)
	        		board.status = -1



		# 0 = border
		# 1 = start
		# 2 = finish
		# 3 = run
		# 4 = to_clear
		# 5 = clear
		# 6 = rubber


	    board.display()

main()





