from Classes.player_class import Player
from Classes.alien_block_class import AlienBlock
from Classes.fortress_class import Fortress
import pygame
import random


def draw_text(win, text_x, text_y, msg, color):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 35)
    text = font.render(f'{msg}', False, color)
    text_rect = text.get_rect(center=(text_x, text_y))

    win.blit(text, text_rect)


# CONSTANTS
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 764
WHITE = (255, 255, 255)

# Variables
running = True
score = 0
level = 1

# Pygame Init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders by PlaceHolderHere")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprites
player_sprite = pygame.image.load('Sprites/Player.png')
player_life_icon = pygame.transform.scale(player_sprite, (48, 48))
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
                    70, 9, 1500)
fortresses = [Fortress(75, 550, 3), Fortress(298, 550, 3),
              Fortress(521, 550, 3)]

while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if player.alive:
                    player.move_right = True
            elif event.key == pygame.K_a:
                if player.alive:
                    player.move_left = True
            elif event.key == pygame.K_SPACE:
                if player.alive:
                    player.shoot()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                if player.alive:
                    player.move_right = False
            elif event.key == pygame.K_a:
                if player.alive:
                    player.move_left = False

    # Background
    WIN.fill((0, 0, 0))

    # HUD
    draw_text(WIN, SCREEN_WIDTH // 2, 40, str(score), WHITE)
    for life_index in range(player.lives):
        WIN.blit(player_life_icon, ((life_index * 56) + 56, 16))

    # Player Respawn Animation
    if player.respawn_cooldown > 0:
        player.respawn_cooldown -= 1
        player.respawn_animation_counter += 1
        if player.respawn_animation_counter > 5:
            player.respawn_animation_counter = 0
            player.respawn_blit = not player.respawn_blit

        if player.respawn_blit:
            player.blit(WIN)

    # Player Processing
    else:
        if player.respawning:
            player.respawning = False
            player.reset(30, SCREEN_HEIGHT - 70)
        elif player.alive:
            player.move()
            # Player Border Collisions
            if player.x < 30:
                player.x = 30
            elif player.x + player.size_x > SCREEN_WIDTH - 30:
                player.x = SCREEN_WIDTH - player.size_x - 30
            player.blit(WIN)
            # Player Bullet
            for bullet_index, bullet in enumerate(player.bullets):
                bullet.move()
                bullet.blit(WIN)
                if bullet.y < -bullet.size_y:  # checks if bullet flew off screen
                    player.bullets.pop(bullet_index)
                else:  # Other Bullet Collisions
                    # Alien Collisions
                    for row in aliens.alien_rows:
                        for alien in row.aliens:
                            if alien.alive:
                                if bullet.is_colliding(alien.get_rect()):
                                    alien.alive = False
                                    aliens.num_alive_aliens -= 1
                                    score += 10
                                    if len(player.bullets) > 0:
                                        player.bullets.pop(bullet_index)
                                        break

                    # Fortress Collisions
                    for fortress in fortresses:
                        if bullet.is_colliding(fortress.get_fortress_rect()):
                            # Calculating Bullet Range for collisions with the fortress
                            lower_bullet_x_range = max(0, (bullet.x - fortress.start_x) // fortress.rect_size)
                            upper_bullet_x_range = min(fortress.num_cols, (
                                        (bullet.x + bullet.size_x - fortress.start_x) // fortress.rect_size) + 1)

                            # Blast Collisions
                            collision_detected = False
                            for row_index in range(fortress.num_rows - 1, 0, -1):
                                if collision_detected:
                                    break
                                else:
                                    for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                                        if fortress.fortress[row_index][col_index] == '1':
                                            colliding_block_x = fortress.start_x + (col_index * fortress.rect_size)
                                            colliding_block_y = fortress.start_y + (row_index * fortress.rect_size)
                                            if bullet.is_colliding(
                                                    pygame.Rect(colliding_block_x, colliding_block_y, fortress.rect_size,
                                                                fortress.rect_size)):

                                                # Calculations for blast radius
                                                # Top Left Coordinates for Blast Radius hit box
                                                blast_x = colliding_block_x - bullet.blast_radius
                                                blast_y = colliding_block_y - bullet.blast_radius

                                                # Blast Ranges
                                                blast_lower_x_range = max(0, (
                                                            (blast_x - fortress.start_x) // fortress.rect_size))
                                                blast_upper_x_range = min(len(fortress.fortress[0]), (blast_x + (
                                                            2 * bullet.blast_radius) - fortress.start_x) //
                                                                          fortress.rect_size + 1)
                                                blast_lower_y_range = max(0, (
                                                            blast_y - fortress.start_y) // fortress.rect_size)
                                                blast_upper_y_range = min(len(fortress.fortress), ((((blast_y + (
                                                            2 * bullet.blast_radius)) - fortress.start_y) //
                                                                        fortress.rect_size) + 1))

                                                # Blast Radius Collisions
                                                for blast_row_index in range(blast_lower_y_range, blast_upper_y_range):
                                                    for blast_col_index in range(blast_lower_x_range, blast_upper_x_range):
                                                        if fortress.fortress[blast_row_index][blast_col_index] == '1':
                                                            x = fortress.start_x + (blast_col_index * fortress.rect_size)
                                                            y = fortress.start_y + (blast_row_index * fortress.rect_size)
                                                            if bullet.blast_calculation(colliding_block_x,
                                                                                        colliding_block_y, x, y,
                                                                                        fortress.rect_size):
                                                                fortress.fortress[blast_row_index][blast_col_index] = 0

                                                # Disabling all collision checks related to this bullet
                                                collision_detected = True
                                                if len(player.bullets) > 0:
                                                    player.bullets.pop(bullet_index)
                                                break
        else:
            if player.lives >= 0:
                aliens.clear_bullets()
                player.alive = True
                player.respawning = True
                player.respawn_cooldown = 120
                player.lives -= 1

        # Alien Processing
        for row in aliens.alien_rows:
            for alien in row.aliens:
                if alien.alive:
                    # Border Collisions
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

                    # Alien bullet processing
                    if alien.bullet_fired:
                        if alien.bullet.y > SCREEN_HEIGHT:  # checks if bullet flew off screen
                            alien.bullet_fired = False
                        else:  # Other Bullet Collisions
                            # Player Collisions
                            if alien.bullet.is_colliding(player.get_rect()):
                                player.alive = False
                                alien.bullet_fired = False

                            # Fortress Collisions
                            for fortress in fortresses:
                                if alien.bullet.is_colliding(fortress.get_fortress_rect()):
                                    # Calculating Bullet Range for collisions with the fortress
                                    lower_bullet_x_range = max(0, (alien.bullet.x - fortress.start_x) // fortress.rect_size)
                                    upper_bullet_x_range = min(fortress.num_cols,
                                                               ((alien.bullet.x + alien.bullet.size_x - fortress.start_x) //
                                                                fortress.rect_size) + 1)

                                    # Blast Collisions
                                    collision_detected = False
                                    for row_index in range(fortress.num_rows - 1, 0, -1):
                                        if collision_detected:
                                            break
                                        else:
                                            for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                                                if fortress.fortress[row_index][col_index] == '1':
                                                    colliding_block_x = fortress.start_x + (
                                                                col_index * fortress.rect_size)
                                                    colliding_block_y = fortress.start_y + (
                                                                row_index * fortress.rect_size)
                                                    if alien.bullet.is_colliding(
                                                            pygame.Rect(colliding_block_x, colliding_block_y,
                                                                        fortress.rect_size,
                                                                        fortress.rect_size)):

                                                        # Calculations for blast radius
                                                        # Top Left Coordinates for Blast Radius hit box
                                                        blast_x = colliding_block_x - alien.bullet.blast_radius
                                                        blast_y = colliding_block_y - alien.bullet.blast_radius

                                                        # Blast Ranges
                                                        blast_lower_x_range = max(0, (
                                                                    (blast_x - fortress.start_x) // fortress.rect_size))
                                                        blast_upper_x_range = min(len(fortress.fortress[0]), (blast_x + (
                                                                2 * alien.bullet.blast_radius) - fortress.start_x) //
                                                                                  fortress.rect_size + 1)
                                                        blast_lower_y_range = max(0, (
                                                                    blast_y - fortress.start_y) // fortress.rect_size)
                                                        blast_upper_y_range = min(len(fortress.fortress), (((blast_y + (
                                                                    2 * alien.bullet.blast_radius)) - fortress.start_y) //
                                                                                    fortress.rect_size) + 1)

                                                        # Blast Radius Collisions
                                                        for blast_row_index in range(blast_lower_y_range,
                                                                                     blast_upper_y_range):
                                                            for blast_col_index in range(blast_lower_x_range,
                                                                                         blast_upper_x_range):
                                                                if fortress.fortress[blast_row_index][blast_col_index] == '1':
                                                                    x = fortress.start_x + (
                                                                                blast_col_index * fortress.rect_size)
                                                                    y = fortress.start_y + (
                                                                                blast_row_index * fortress.rect_size)
                                                                    if alien.bullet.blast_calculation(colliding_block_x,
                                                                                                      colliding_block_y, x,
                                                                                                      y,
                                                                                                      fortress.rect_size):
                                                                        fortress.fortress[blast_row_index][
                                                                            blast_col_index] = 0

                                                        # Disabling further collision checks
                                                        alien.bullet_fired = False
                                                        collision_detected = True
                                                        break

                        alien.bullet.move()
                        alien.bullet.blit(WIN)

                    # Alien Firing
                    elif not alien.bullet_fired:
                        if random.randint(0, aliens.global_firing_chance - (
                                (aliens.TOTAL_NUM_ALIENS - aliens.num_alive_aliens) * 5)) == 0:
                            alien.shoot()
        # Alien Rendering
        aliens.blit(WIN)

        # Alien Reset
        if aliens.num_alive_aliens <= 0:
            level += 1
            aliens.reset()
            # Fortress Reset
            for fortress in fortresses:
                fortress.reset_fortress()

        # Fortresses Blit
        for fortress in fortresses:
            fortress.blit(WIN)

    pygame.display.update()
