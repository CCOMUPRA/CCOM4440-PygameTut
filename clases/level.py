import pygame
from clases.enemy import Enemy
# from clases.decision import *
from clases.platform import Platform
import random

class Level:
    def __init__(self, player):
        self.enemy_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0

    def startGame(self, width, height):
        # Add all objects
        for i in range(5):
            block = Enemy((255, 0, 0), 100, 100)

            block.rect.x = random.randrange(width)
            block.rect.y = random.randrange(height)

            # block.set_decision_tree(create_decision_tree())

            self.enemy_list.add(block)
            self.all_sprites.add(block)

        # Add all level platforms
        # Array with width, height, x, and y of platform
        level = [[100, 70, 50, 300],
                 [100, 70, 150, 350],
                 [100, 70, 100, 200],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        self.all_sprites.add(self.player)

    def restartGame(self, width, height):
        self.player.rect.x = 0
        self.player.rect.y = 0
        self.enemy_list.empty()
        self.all_sprites.empty()
        self.platform_list.empty()
        self.startGame(width, height)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.enemy_list.draw(screen)
        self.platform_list.draw(screen)
        self.all_sprites.draw(screen)

    def checkFinished(self):
        if len(self.enemy_list) == 0:
            return True
        else:
            return False

    def eat(self):
        sprite_hit = pygame.sprite.spritecollide(self.player, self.enemy_list, True)
        point = 0
        if sprite_hit:
            point = point + 1
        return point

    def collide_big_enemy(self, big_enemy):
        if big_enemy.colliderect(self.player.rect):
            return True
        return False

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
