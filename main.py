import pygame, sys, random
import pygame_gui

from clases.enemy import Enemy
# from clases.decision import *
from clases.player import Player
from clases.level import Level

pygame.init()
# OTRO COMENTARIO BONITO
# Manejar el pacing
mainClock = pygame.time.Clock()

# Window
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Collision Detection")

# UI
manager = pygame_gui.UIManager((WINDOWWIDTH, WINDOWHEIGHT))
button_layout_rect = pygame.Rect((WINDOWWIDTH-100)/2,(WINDOWHEIGHT-20)/2,100,20)

start_game_btn = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text="Start game", manager=manager)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# DECLARE ENEMIES
big_enemy = pygame.Rect(200, 100, 70, 70)
enemy_speed = [2, 2]
enemy_list = pygame.sprite.Group()

# DECLARE PLAYER
player = Player(WINDOWWIDTH, WINDOWHEIGHT)
x_speed = 2
y_speed = 2

all_sprites = pygame.sprite.Group()

# Old logic
# Add all objects
for i in range(5):
    block = Enemy((0, 255, 0), 200, 100)

    block.rect.x = random.randrange(WINDOWWIDTH)
    block.rect.y = random.randrange(WINDOWHEIGHT)

    # block.set_decision_tree(create_decision_tree())
    enemy_list.add(block)
    all_sprites.add(block)

all_sprites.add(player)

# LEVELS LOGIC
levels = [Level(player), Level(player)]
current_level_no = 0
current_level = levels[current_level_no]

player.level = current_level

current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)

# FONTS
font = pygame.font.Font("Space Crusaders.otf", 28)

# OTHER VARS
done = False
displayInstructions = True
instructionsPage = 1

pygame.mixer.music.load("lady-of-the-80.mp3")
pygame.mixer.music.set_volume(0.1)

bump = pygame.mixer.Sound("game-start.mp3")

while not done and displayInstructions:
    time_delta = mainClock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            instructionsPage += 1
            if instructionsPage == 3:
                displayInstructions = False
                pygame.mixer.music.play()
        manager.process_events(event)

    screen.fill((0, 0, 0))

    if instructionsPage == 1:
        text = font.render("Instructions", True, (255, 255, 255))
        screen.blit(text, [50, 0])

        text = font.render("Eres un bloque, good luck", True, (255, 255, 255))
        screen.blit(text, [50, 20])

    if instructionsPage == 2:
        text = font.render("Instructions 2", True, (255, 255, 255))
        screen.blit(text, [50, 0])

        text = font.render("No choques", True, (255, 255, 255))
        screen.blit(text, [50, 20])

    mainClock.tick(60)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

# movement
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

points = 0

# run the game loop
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    big_enemy.x += enemy_speed[0]
    big_enemy.y += enemy_speed[1]

    current_level.player.move()
    current_level.enemy_list.update(current_level.player)

    # Manejar movimiento del enemigo
    big_enemy = big_enemy.move(enemy_speed)
    if big_enemy.left <= 0 or big_enemy.right >= WINDOWWIDTH:
        enemy_speed[0] *= -1
    elif big_enemy.top <= 0 or big_enemy.bottom >= WINDOWHEIGHT:
        enemy_speed[1] *= -1

    collideThreshold = 10
    if big_enemy.colliderect(current_level.player):
        print("CHOQUÉ")
        pygame.draw.rect(screen, (255, 0, 0), current_level.player, 4)
        pygame.mixer.Sound.play(bump)
        # Added enemy speed check to manage the same collision happening in every frame.
        if abs(current_level.player.rect.bottom - big_enemy.top) < collideThreshold and enemy_speed[1] < 0:
            enemy_speed[1] *= -1
        elif abs(current_level.player.rect.top - big_enemy.bottom) < collideThreshold and enemy_speed[1] > 0:
            enemy_speed[1] *= -1
        elif abs(current_level.player.rect.right - big_enemy.left) < collideThreshold and enemy_speed[0] < 0:
            enemy_speed[0] *= -1
        elif abs(current_level.player.rect.left - big_enemy.right) < collideThreshold and enemy_speed[0] > 0:
            enemy_speed[0] *= -1

    # If the player gets near the right side, shift the world left.
    if player.rect.right >= 500:
        diff = player.rect.right - 500
        player.rect.right = 500
        current_level.shift_world(-diff)

    # If the player gets near the left side, shift the world right
    if player.rect.left <= 100:
        diff = 100 - player.rect.left
        player.rect.left = 100
        current_level.shift_world(diff)

    # Levels logic
    current_level.draw(screen)

    points = points + current_level.eat()

    text = font.render(str(points), True, WHITE)
    screen.blit(text, [10, 10])

    lost = current_level.collide_big_enemy(big_enemy)

    if lost:
        points = 0
        current_level.restartGame(WINDOWWIDTH, WINDOWHEIGHT)

    if points == 5:
        current_level_no = 1
        current_level = levels[current_level_no]
        current_level.startGame(WINDOWWIDTH, WINDOWHEIGHT)
    # points = 0

    pygame.draw.rect(screen, (0, 255, 0), big_enemy)

    # FPS
    mainClock.tick(60)

    pygame.display.flip()
