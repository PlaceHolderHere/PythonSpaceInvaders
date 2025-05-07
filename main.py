from Classes.player_class import Player
from Classes.alien_block_class import AlienBlock
from Classes.fortress_class import Fortress
import pygame

# CONSTANTS
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 764

# Variables
running = True
score = 0

# Pygame Init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders by PlaceHolderHere")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprites
player_sprite = pygame.image.load('Sprites/Player.png')
player_bullet_sprite = pygame.image.load('Sprites/bullet.png')
alien_sprite1 = pygame.image.load('Sprites/enemy1.png')
alien_sprite2 = pygame.image.load('Sprites/enemy2.png')
alien_sprite3 = pygame.image.load('Sprites/enemy3.png')
alien_sprite4 = pygame.image.load('Sprites/enemy4.png')
alien_bullet = pygame.image.load('Sprites/enemy_bullet.png')
alien_sprites = (alien_sprite4, alien_sprite3, alien_sprite2, alien_sprite1, alien_sprite1)

# Player
player = Player(30, SCREEN_HEIGHT - 70, player_sprite, player_bullet_sprite)
aliens = AlienBlock(30, ([100 + i * 70 for i in range(5)]), alien_sprites, alien_bullet, 90,
                    70, 7)
fortresses = [Fortress(75, 550, 3), Fortress(298, 550, 3),
              Fortress(521, 550, 3)]

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

    # Background
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
        if bullet.y < -bullet.size_y:  # checks if bullet flew off screen
            player.bullets.pop(bullet_index)
        else:
            # Collisions with Aliens
            for row in aliens.alien_rows:
                for alien in row.aliens:
                    if alien.alive:
                        if bullet.is_colliding(pygame.Rect(alien.x, alien.y, alien.size_x, alien.size_y)):
                            alien.alive = False
                            aliens.num_aliens -= 1
                            score += 10
                            if len(player.bullets) > 0:
                                player.bullets.pop(bullet_index)
                                break

            # Collisions with Fortress
            for fortress in fortresses:
                if bullet.is_colliding(
                        pygame.Rect(fortress.start_x, fortress.start_y, len(fortress.fortress[0]) * fortress.rect_size,
                                    len(fortress.fortress) * fortress.rect_size)):

                    # Calculating Bullet Range for collisions with the fortress
                    if bullet.x < fortress.start_x:
                        lower_bullet_x_range = 0
                    else:
                        lower_bullet_x_range = (bullet.x - fortress.start_x) // fortress.rect_size

                    if bullet.x + bullet.size_x > fortress.start_x + (len(fortress.fortress[0]) * fortress.rect_size):
                        upper_bullet_x_range = len(fortress.fortress[0])
                    else:
                        upper_bullet_x_range = ((bullet.x + bullet.size_x - fortress.start_x) // fortress.rect_size) + 1

                    hit = False
                    for row_index in range(len(fortress.fortress) - 1, 0, -1):
                        if hit:
                            break

                        for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                            if fortress.fortress[row_index][col_index] == 1:
                                block_x = fortress.start_x + (col_index * fortress.rect_size)
                                block_y = fortress.start_y + (row_index * fortress.rect_size)

                                if bullet.is_colliding(pygame.Rect(block_x, block_y,
                                                                   fortress.rect_size, fortress.rect_size)):
                                    # Calculations for blast radius
                                    # Top Left Coordinates for Blast Radius hit box
                                    blast_x = bullet.x + (bullet.size_x // 2) - bullet.blast_radius
                                    blast_y = bullet.y - bullet.blast_radius

                                    # Lower x range
                                    if blast_x < fortress.start_x:
                                        blast_lower_x_range = 0
                                    else:
                                        blast_lower_x_range = (blast_x - fortress.start_x) // fortress.rect_size

                                    # Upper x range
                                    if blast_x + (2 * bullet.blast_radius) > fortress.start_x + (
                                            len(fortress.fortress[0])) * fortress.rect_size:
                                        blast_upper_x_range = len(fortress.fortress[0])
                                    else:
                                        blast_upper_x_range = (((blast_x + (2 * bullet.blast_radius)) -
                                                                fortress.start_x) // fortress.rect_size) + 1

                                    # Lower y range
                                    if blast_y < fortress.start_y:
                                        blast_lower_y_range = 0
                                    else:
                                        blast_lower_y_range = (blast_y - fortress.start_y) // fortress.rect_size

                                    # Upper y range
                                    if blast_y + (2 * bullet.blast_radius) > fortress.start_y + (
                                            len(fortress.fortress) * fortress.rect_size):
                                        blast_upper_y_range = len(fortress.fortress)
                                    else:
                                        blast_upper_y_range = ((((blast_y + (
                                                2 * bullet.blast_radius)) - fortress.start_y) // fortress.rect_size)
                                                               + 1)

                                    for blast_row_index in range(blast_lower_y_range, blast_upper_y_range - 1):
                                        for blast_col_index in range(blast_lower_x_range, blast_upper_x_range):
                                            if fortress.fortress[blast_row_index][blast_col_index] == 1:
                                                x = fortress.start_x + (blast_col_index * fortress.rect_size)
                                                y = fortress.start_y + (blast_row_index * fortress.rect_size)
                                                if bullet.blast_calculation(x, y, fortress.rect_size, fortress.rect_size):
                                                    fortress.fortress[blast_row_index][blast_col_index] = 0

                                    hit = True
                                    if len(player.bullets) > 0:
                                        player.bullets.pop(bullet_index)
                                    break

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

    # Fortresses Blit
    for fortress in fortresses:
        fortress.blit(WIN)

    if aliens.num_aliens <= 0:
        aliens.reset()

    pygame.display.update()
