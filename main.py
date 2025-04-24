from Classes.player_class import Player
from Classes.alien_class import Alien
import pygame

# CONSTANTS
SCREEN_HEIGHT = 704
SCREEN_WIDTH = 704

# Variables
running = True

# Pygame Init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders by PlaceHolderHere")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Player
player = Player(0, 630, pygame.image.load('Sprites/Player.png'), pygame.image.load('Sprites/bullet.png'))
alien = Alien(0, 100, pygame.image.load('Sprites/enemy1.png'), 0, 120, pygame.image.load('Sprites/enemy_bullet.png'))

while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player.move_right = True
            elif event.key == pygame.K_a:
                player.move_left = True
            elif event.key == pygame.K_SPACE:
                player.shoot()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player.move_right = False
            elif event.key == pygame.K_a:
                player.move_left = False

    WIN.fill((0, 0, 0))

    # Player Processing
    player.move()
    # Player Border Collisions
    if player.x < 0:
        player.x = 0
    elif player.x + player.size_x > SCREEN_WIDTH:
        player.x = SCREEN_WIDTH - player.size_x

    # Player Bullet
    for bullet in player.bullets:
        bullet.blit(WIN)

    player.blit(WIN)

    # Alien Processing
    alien.blit(WIN)

    pygame.display.update()
