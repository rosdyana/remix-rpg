from tkinter import E
import pygame
from settings import *


class MenuItem:
	def __init__(self, left, top, width, height, index, font):
		self.rect = pygame.Rect(left, top, width, height)
		self.index = index
		self.font = font

	def display_names(self, surface, name, cost, selected):
		color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

		title_surface = self.font.render(str(cost), True, color)
		title_rect = title_surface.get_rect(
			midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))
		surface.blit(title_surface, title_rect)

		title_surface = self.font.render(name, True, color)
		title_rect = title_surface.get_rect(
			midtop=self.rect.midtop + pygame.math.Vector2(0, 20))
		surface.blit(title_surface, title_rect)

	def display_bar(self, surface, value, max_value, selected):
		color = BAR_COLOR_SELECTED if selected else BAR_COLOR
		top = self.rect.midtop + pygame.math.Vector2(0, 60)
		bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
		full_height = bottom.y - top.y
		relative_number = (value / max_value) * full_height
		value_rect = pygame.Rect(
			top[0] - 15, bottom[1] - relative_number, 30, 10)
		pygame.draw.line(surface, color, top, bottom, 5)
		pygame.draw.rect(surface, color, value_rect)

	def trigger(self, player):
		upgrade_attribute = list(player.stats.keys())[self.index]

		if player.exp >= player.upgrade_costs[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
			player.exp -= player.upgrade_costs[upgrade_attribute]
			player.stats[upgrade_attribute] *= 1.2
			player.upgrade_costs[upgrade_attribute] *= 1.4

		if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
			player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

	def display(self, surface, selection_num, name, value, max_value, cost):
		if self.index == selection_num:
			pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
		else:
			pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
			pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

		self.display_names(surface, name, cost, self.index == selection_num)
		self.display_bar(surface, value, max_value, self.index == selection_num)
