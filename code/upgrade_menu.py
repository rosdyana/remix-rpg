import pygame
from menu_item import MenuItem
from settings import *


class UpgradeMenu:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)

        self.selection_index = 0
        self.selection_time = None
        self.can_select = True

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_menu_item()

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_select:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_select = True

    def create_menu_item(self):
        self.item_list = []
        for index, item in enumerate(range(self.attribute_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2
            top = self.display_surface.get_size()[1] * 0.1
            item = MenuItem(left, top, self.width,
                            self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)
