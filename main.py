# our game imports
import pygame, sys, random, time
from db import Storage
import menu
from pygame import mixer
from tkinter import *

# check for initializing errors
check_errors = pygame.init()
mixer.init()
if check_errors[1] > 0:
	print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
	sys.exit(-1)
else:
	print("(+) PyGame successfully initialized!")


# Play surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake game!')
vibes = mixer.music.load('./assets/audio/SKYBOX.ogg')
mixer.music.set_volume(0.3)

# Colors
red = pygame.Color(255, 0, 0) # gameover
green = pygame.Color(0, 255, 0) #snake
black = pygame.Color(0, 0, 0) #score
white = pygame.Color(255, 255, 255) #background
brown = pygame.Color(165, 42, 42) #food
gold = pygame.Color("#aca17d")

# FPS controller
fpsController = pygame.time.Clock()

# Important varibles
snakePos = [100, 50] #Snake initial position
snakeBody = [[100,50], [90,50], [80,50]] #Snake Body
SNAKE_WIDTH = 10

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0

def register_user():
	# Create a Tkinter object
	root = Tk()
	root.geometry("180x180+720+260")
	root.resizable(0,0)

	name_label = Label(root, text="Name: ")
	name_label.grid(row=0, column=0)
	name_textbox = Entry(root)
	name_textbox.grid(row=0, column=1)


	def get_name_and_close():
		global name
		name = name_textbox.get()
		# prompt the user to reenter the name if the name is empty
		if name == "":
			name_textbox.delete(0, END)
			name_textbox.insert(0, "Please enter your name!")
			name_textbox.config(fg="red")
			name_textbox.focus()
			name = name_textbox.get()
		root.destroy()
		return name

	reg_btn = Button(root, text="Register", command=get_name_and_close, background="green", foreground="white")
	reg_btn.grid(row=1, column=1)

	# Run the mainloop
	root.mainloop()
	return name

# Game over function
def gameOver():
	global started
	myFont = pygame.font.SysFont('monaco', 72)
	HOFont = pygame.font.SysFont('Arial', 30)
	GOsurf = myFont.render('Game over!', True, red)
	GOrect = GOsurf.get_rect()
	
	user_db = Storage(user)
	user_db.update(score)
	hi_score = user_db.read_highscore()	

	HOsurf = HOFont.render(f"The overall highscore is: {hi_score['best_score']} was last set by {hi_score['set_by']}", True, gold)
	HOrect = HOsurf.get_rect()

	GOrect.midtop = (360, 15)
	HOrect.midtop = (360, 55)
	playSurface.fill(white)
	playSurface.blit(GOsurf,GOrect)
	playSurface.blit(HOsurf, HOrect)
	showScore(0)
	pygame.display.flip()
	mixer.music.stop()
	time.sleep(4)
	pygame.quit() #pygame exit
	sys.exit() #console exit
	

def showScore(choice=1):
	sFont = pygame.font.SysFont('monaco', 24)
	Ssurf = sFont.render('Score : {0}'.format(score) , True, black)
	Srect = Ssurf.get_rect()
	if choice == 1:
		Srect.midtop = (80, 10)
	else:
		Srect.midtop = (360, 120)
	playSurface.blit(Ssurf,Srect)


# Time complexity: unknown
# This is the faster method, but I prefer drawing lines
def drawGrid():
	for i in range(0, playSurface.get_width() // SNAKE_WIDTH):
		for j in range(0, playSurface.get_height() // SNAKE_WIDTH):
			rect = pygame.Rect(i*SNAKE_WIDTH, j*SNAKE_WIDTH, SNAKE_WIDTH, SNAKE_WIDTH)
			pygame.draw.rect(playSurface, (190,190,190), rect, 1)


# Time complexity: O(n)
# This is the slower method to create a grid
def drawWithLines():
	for i in range(0, playSurface.get_width(), SNAKE_WIDTH):
		for j in range(0, playSurface.get_width(), SNAKE_WIDTH):
			if i % 3 == 0:
				pygame.draw.line(playSurface, (255, 165, 0), (i, j),(i, j - SNAKE_WIDTH))
				pygame.draw.line(playSurface, (255, 165, 0), (0, j),(playSurface.get_width(), j)) # Horizontal line
			else:
				pygame.draw.line(playSurface, black, (i, j),(i, j - SNAKE_WIDTH))
				pygame.draw.line(playSurface, black, (0, j),(playSurface.get_width(), j)) # Horizontal line


muted = False
m = menu.Menu()
play_button = menu.Button(playSurface, 'Play', (300, 200), (200, 50), (170, 201, 241))
m.draw_menu()
play_button.draw()
user = register_user()
paused = True
started = True
mixer.music.play(-1)
# Main Logic of the game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == ord('d'):
				changeto = 'RIGHT' 
			if event.key == pygame.K_LEFT or event.key == ord('a'):
				changeto = 'LEFT' 
			if event.key == pygame.K_UP or event.key == ord('w'):
				changeto = 'UP' 
			if event.key == pygame.K_DOWN or event.key == ord('s'):
				changeto = 'DOWN' 
			if event.key == pygame.K_m or event.key == ord('m'):
				if not muted:
					muted = True
					mixer.music.set_volume(0)
				else:
					muted = False
					mixer.music.set_volume(0.3)

			if event.key == pygame.K_p or event.key == ord('p'):
				paused = not paused
				# play_button.draw(True)
				if paused:
					mixer.music.pause()
					m.draw_menu()
					play_button.draw()
				else:
					mixer.music.unpause()
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	if not paused:
		# validation of direction
		if changeto == 'RIGHT' and not direction == 'LEFT':
			direction = 'RIGHT'
		if changeto == 'LEFT' and not direction == 'RIGHT':
			direction = 'LEFT'
		if changeto == 'UP' and not direction == 'DOWN':
			direction = 'UP'
		if changeto == 'DOWN' and not direction == 'UP':
			direction = 'DOWN'

		# Update snake position [x,y]
		if direction == 'RIGHT':
			snakePos[0] += 10
		if direction == 'LEFT':
			snakePos[0] -= 10
		if direction == 'UP':
			snakePos[1] -= 10
		if direction == 'DOWN':
			snakePos[1] += 10
		
		
		# Snake body mechanism
		snakeBody.insert(0, list(snakePos))
		if (snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]):
			score += 1
			foodSpawn = False
		else:
			snakeBody.pop()
			
		#Food Spawn
		if foodSpawn == False:
			foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] 
		foodSpawn = True
		
		#Background
		playSurface.fill((202, 228, 241))
		# drawWithLines()
		drawGrid()


		#Draw Snake 
		for pos in snakeBody:
			pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
		
		pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1],10,10))
		
		# Bound
		if snakePos[0] > 710 or snakePos[0] < 0:
			gameOver()
		if snakePos[1] > 450 or snakePos[1] < 0:
			gameOver()
			
		# Self hit
		for block in snakeBody[1:]:
			if snakePos[0] == block[0] and snakePos[1] == block[1]:
				gameOver()
		
		#common stuff
		showScore()

	pygame.display.flip()
	fpsController.tick(15)
	
