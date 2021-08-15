import pygame
import importlib
pygame.init()

# Loading main window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAIN")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont('comicsans', 50)

class Button:
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.text_color = BLACK
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw(self, win, outline):
		if outline:
			pygame.draw.rect(win, self.color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

		if self.text != '':
			text = FONT.render(self.text, 1, self.text_color)
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True

		return False

def redraw_window(buttons):
	WIN.fill(BLACK)
	for button in buttons:
		button.draw(WIN, WHITE)

def multiplayer(counter):
	import client

	if counter > 0:
		importlib.reload(client)

	msg = client.send("OK", False)

	if msg == "RED":
		import main_red

	elif msg == "YELLOW":
		import main_yellow

def main(counter=0):
	run = True

	multiplayer_button = Button(WHITE, (WIDTH - 250)//2, (HEIGHT - 75)//2, 250, 50, "Multiplayer")

	while run:
		redraw_window([multiplayer_button])
		pygame.display.update()

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if multiplayer_button.isOver(pos):
					run = False
					pygame.quit()
					multiplayer(counter)

			if event.type == pygame.MOUSEMOTION:
				if multiplayer_button.isOver(pos):
					multiplayer_button.color = BLACK
					multiplayer_button.text_color = WHITE
				else:
					multiplayer_button.color = WHITE
					multiplayer_button.text_color = BLACK
	
	pygame.quit()

if __name__ == "__main__":
	main()