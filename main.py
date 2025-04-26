from Classes.player_class import Player
from Classes.alien_class import Alien
from Classes.alien_block_class import AlienBlock
import pygame

# CONSTANTS
SCREEN_HEIGHT = 764
SCREEN_WIDTH = 764

# Variables
running = True

# Pygame Init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders by PlaceHolderHere")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Player
player = Player(30, 680, pygame.image.load('Sprites/Player.png'), pygame.image.load('Sprites/bullet.png'))
aliens = AlienBlock(30, ([30 + i * 70 for i in range(5)]),
                    (pygame.image.load('Sprites/enemy4.png'), pygame.image.load('Sprites/enemy3.png'),
                     pygame.image.load('Sprites/enemy2.png'), pygame.image.load('Sprites/enemy1.png'),
                     pygame.image.load('Sprites/enemy1.png')), pygame.image.load('Sprites/enemy_bullet.png'),
                    90, 70, 7)

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
    if player.x < 30:
        player.x = 30
    elif player.x + player.size_x > SCREEN_WIDTH - 30:
        player.x = SCREEN_WIDTH - player.size_x - 30

    # Player Bullet
    for bullet_index, bullet in enumerate(player.bullets):
        bullet.move()
        if bullet.y < -bullet.size_y:
            player.bullets.pop(bullet_index)
        else:
            for row in aliens.alien_rows:
                # Potential Optimization
                'if row.aliens[0].y + row.aliens[0].size_y < bullet.y and bullet.y + bullet.size_y > row.aliens[0].y:'
                for alien in row.aliens:
                    if alien.alive:
                        if bullet.is_colliding(pygame.Rect(alien.x, alien.y, alien.size_x, alien.size_y)):
                            alien.alive = False
                            aliens.num_aliens -= 1
                            if len(player.bullets) > 0:
                                player.bullets.pop(bullet_index)


        bullet.blit(WIN)

    player.blit(WIN)

    # Alien Processing
    # Alien Wall Collisions
    for row in aliens.alien_rows:
        for alien in row.aliens:
            if alien.x + alien.size_x > SCREEN_WIDTH:
                row.move_down()
                x_change = alien.x + alien.size_x - SCREEN_WIDTH
                for alien2 in row.aliens:
                    alien2.x -= x_change
                break
            elif alien.x < 30:
                row.move_down()
                x_change = 30 - alien.x
                for alien2 in row.aliens:
                    alien2.x += x_change
                break

    aliens.blit(WIN)

    if aliens.num_aliens <= 0:
        aliens.reset()

    pygame.display.update()
