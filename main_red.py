import pygame
import os
import client
import json
pygame.font.init()
pygame.mixer.init()

# Loading main window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RED MAIN")

# Loading colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Loading speeds
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 7

DISCONNECT_MESSAGE = "!DISCONNECT"

# Loading Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 90)

# Loading special events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Loading Dimensions
BORDER = pygame.Rect((WIDTH-10)//2, 0, 10, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Loading Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))

# Loading Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90+180)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

# Making ship class
class Ship:

	# Inintialising all the variables used
	def __init__(self, x, y, color):
		self.color = color
		self.x = x
		self.y = y
		self.hitbox = pygame.Rect(self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
		self.bullets = []
		self.health = 10
		self.width = self.hitbox.width
		self.height = self.hitbox.height
		self.cooldown = 0

	# making sure the hitbox moves with ship
	def update_hitbox(self):
		self.hitbox = pygame.Rect(self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	# handling movement of the ship
	def handle_movement(self, keys_pressed):
		if self.color == "red":
			if keys_pressed[pygame.K_a] and self.x - VEL > BORDER.x + BORDER.width:
				self.x -= VEL
			if keys_pressed[pygame.K_d] and self.x + VEL + self.width < WIDTH:
				self.x += VEL
			if keys_pressed[pygame.K_s] and self.y + VEL + self.height < HEIGHT - 15:
				self.y += VEL
			if keys_pressed[pygame.K_w] and self.y - VEL > 0:
				self.y -= VEL

		self.update_hitbox()

	# gotta make the bullet move, right?
	def handle_bullets(self, opposing):
		if self.color == "yellow":
			for bullet in self.bullets:
				if opposing.hitbox.colliderect(bullet):
					pygame.event.post(pygame.event.Event(RED_HIT))
		
		elif self.color == "red":
			for bullet in self.bullets:
				bullet.x -= BULLET_VEL
				if opposing.hitbox.colliderect(bullet):
					self.cooldown += 1
					if self.cooldown == 2:
						self.bullets.remove(bullet)
						self.cooldown = 0

				elif bullet.x < 0:
					self.bullets.remove(bullet)

# drawing the window
def draw_window(red, yellow):
	WIN.blit(SPACE, (0, 0))
	pygame.draw.rect(WIN, BLACK, BORDER)

	red_health_text = HEALTH_FONT.render("Health: " + str(red.health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow.health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
	WIN.blit(yellow_health_text, (10, 10))

	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))

	for bullet in red.bullets:
		pygame.draw.rect(WIN, RED, bullet)

	for bullet in yellow.bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)

	pygame.display.update()

# drawing the winner
def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()//2))
	pygame.display.update()
	pygame.time.delay(5000)

# drawing tutorial
def draw_tutorial(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()//2))
	pygame.display.update()
	pygame.time.delay(5000)

# main function
def main():
	red = Ship(700, 300, "red")
	yellow = Ship(100, 300, "yellow")

	clock = pygame.time.Clock()

	run = True
	winner_text_real = ""
	winner_text = ""

	calm_down = 0

	draw_tutorial("YOU ARE RED (right side)")
	while run:
		clock.tick(FPS)

		bullets = []
		for x in red.bullets:
			bullets.append(f"{x.x},{x.y}")

		arguments = [red.x, red.y, bullets, red.health, winner_text]
		arguments = json.dumps(arguments)
		yellow_obj = client.send(arguments)

		if yellow_obj == DISCONNECT_MESSAGE:
			import main
			main.main(10)

		yellow_obj = json.loads(yellow_obj)
		yellow.x, yellow.y = int(yellow_obj[0]), int(yellow_obj[1])
		yellow.bullets = yellow_obj[2]
		yellow.health = int(yellow_obj[3])
		winner_text_real = yellow_obj[4]

		for bullet in range(0, len(yellow.bullets)):
			yellow.bullets[bullet] = yellow.bullets[bullet].split(",")
			yellow.bullets[bullet] = pygame.Rect(int(yellow.bullets[bullet][0]), int(yellow.bullets[bullet][1]), 10, 5)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and len(red.bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
					red.bullets.append(bullet)
					# BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				red.health -= 1
				# BULLET_HIT_SOUND.play()

		if red.health <= 0:
			calm_down += 1
			if calm_down == 2:
				winner_text = "Yellow has won"

		if yellow.health <= 0:
			calm_down += 2
			if calm_down == 2:
				winner_text = "Red has won"

		if winner_text_real != "":
			client.send(arguments)
			draw_winner(winner_text)
			import main
			main.main(1)

		keys_pressed = pygame.key.get_pressed()
		red.handle_movement(keys_pressed)

		yellow.handle_bullets(red)
		red.handle_bullets(yellow)
		yellow.update_hitbox()
		red.update_hitbox()

		draw_window(red, yellow)

	pygame.quit()

main()