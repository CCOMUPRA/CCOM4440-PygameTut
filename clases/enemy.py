import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.state = "idle"
        self.evade_obj = None

    def set_state(self, state, evade_obj):
        self.state = state
        if state == "evade":
            self.evade_obj = evade_obj

    def update(self, player):
        if self.state == "idle":
            # self.rect.x = self.rect.x + random.randint(0, 10)
            # self.rect.y = self.rect.y - random.randint(0, 10)
            # # Verifico todo el tiempo si el player me va a dar
            dx = abs(player.rect.x - self.rect.x)
            dy = abs(player.rect.y - self.rect.y)
            dist = math.sqrt((dx ** 2) + (dy ** 2))

            # print("DISTANCIA ", dist)

            if dist < 100:
                print("EVADIR")
                self.set_state("evade", player)

        elif self.state == "evade":
            self.rect.x = self.rect.x + (player.change_x/2)
            self.rect.y = self.rect.y + (player.change_y/2)

