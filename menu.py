from typing import Tuple
import pygame
from pygame import Surface

class Button:
	def __init__(self, surf: Surface, text: str, coords: Tuple[int], size: Tuple[int], bg='black'):
		self.x, self.y = coords
		self.width, self.height = size
		self.text = text
		self.font = pygame.font.Font('assets/fonts/playfair_italic.ttf', 30)
		# Make a rectangle for the button
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.surface = surf
		self.bg = bg
		self.clicked = False
		self.click()	

	def draw(self, border=False):
		# Draw the button
		self.textBox = self.font.render(self.text, True, (180, 205, 255))
		self.size = self.textBox.get_size()
		pygame.draw.rect(self.surface, self.bg, self.rect)
		# Draw the border
		if border:
			pygame.draw.rect(self.surface, (255, 255, 255), self.rect, 1)

		self.surface.blit(self.textBox, (self.x + self.width / 2 - self.font.size(self.text)[0] / 2, self.y + self.height / 2 - self.font.size(self.text)[1] / 2))
		pygame.display.update(self.rect)


	def click(self):
		print('Clicked')
		pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
					if self.rect.collidepoint(pos):
						self.clicked = True
						print('Clicked')
						# return True
		# return False





class Menu:
	def __init__(self):
		self.screen = pygame.display.set_mode((720, 460))
		self.menu_items = []
		self.screen.fill((255, 255, 255))
		self.screen.blit(pygame.image.load('assets/images/main_menu.png'), (0, 0))
		# self.screen.blit(pygame.image.load('assets/images/snake_title.png'), (0, 0))
		pygame.display.flip()
		self.running = True
		self.menu_items = ['Play', 'Exit', 'Settings']
		self.menu_index = 0
		self.menu_font = pygame.font.Font('assets/fonts/playfair_italic.ttf', 30)
		self.menu_font_selected = pygame.font.Font('assets/fonts/playfair_italic.ttf', 40)
		self.menu_font_selected_color = (255, 0, 0)
		# self.btn = Button(self.screen, 'Play', (300, 200), (100, 50))
		# button2 = Button(self.screen, 'Exit', (300, 250), (200, 50))
	
	def draw_menu(self):
		self.screen.blit(pygame.image.load('assets/images/main_menu.png'), (0, 0))
		# self.btn.draw(True)
		# self.btn.click()
		for i in range(len(self.menu_items)):
			if i == self.menu_index:
				self.screen.blit(self.menu_font_selected.render(self.menu_items[i], True, self.menu_font_selected_color), (100, 100 + i * 50))
			else:
				self.screen.blit(self.menu_font.render(self.menu_items[i], True, (0, 0, 255)), (100, 100 + i * 50))
		# self.screen.fill((255, 255, 255))
		pygame.display.flip()



