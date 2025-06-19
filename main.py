from Classes.player_class import Player
from Classes.alien_block_class import AlienBlock
from Classes.fortress_class import Fortress
from Classes.button_class import Button
import pygame
import random


def draw_text(win, text_x, text_y, msg, color):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 35)
    text = font.render(f'{str(msg)}', False, color)
    text_rect = text.get_rect(center=(text_x, text_y))

    win.blit(text, text_rect)


def get_lower_bound(lower_x, upper_x, block_size):
    return max(0, (upper_x - lower_x) // block_size)


def get_upper_bound(lower_x, upper_x, block_size, max_output):
    return min(max_output, (upper_x - lower_x) // block_size + 1)


# CONSTANTS
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 764
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MIN_ALIEN_FIRING_CHANCE = 10
MIN_ALIEN_MOVEMENT_TRIGGER = 40
FPS = 60

# Variables
running = True
score = 0
level = 1
current_menu = 'HOME'
aliens_move_down = False
new_level_animation_cooldown = 0
new_level_animation_counter = 0
new_level_blit_animation = False

# Pygame Init
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders by PlaceHolderHere")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# SFX
player_fire_SFX = pygame.mixer.Sound("SFX/player_fire.wav")
player_death_SFX = pygame.mixer.Sound("SFX/player_death.wav")
alien_death_SFX = pygame.mixer.Sound("SFX/alien_death.wav")

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

# Buttons
play_button = Button(SCREEN_WIDTH // 2, 302, pygame.image.load("Buttons/Play.png"))
controls_button = Button(SCREEN_WIDTH // 2, 400, pygame.image.load("Buttons/Controls.png"))
main_menu_button = Button(SCREEN_WIDTH // 2, 124, pygame.image.load("Buttons/Main Menu.png"))
resume_button = Button(SCREEN_WIDTH // 2, 222, pygame.image.load("Buttons/Resume.png"))
restart_button = Button(SCREEN_WIDTH // 2, 320, pygame.image.load("Buttons/Restart.png"))
quit_button = Button(SCREEN_WIDTH // 2, 400, pygame.image.load("Buttons/Quit.png"))
main_menu_defeat_button = Button(SCREEN_WIDTH // 2, 352, pygame.image.load("Buttons/Main Menu.png"))
retry_Button = Button(SCREEN_WIDTH // 2, 448, pygame.image.load("Buttons/Retry.png"))

# Game Objects
player = Player(30, SCREEN_HEIGHT - 70, player_sprite, player_bullet_sprite)
aliens = AlienBlock(60, ([100 + i * 70 for i in range(5)]), alien_sprites, alien_bullet, 90,
                    70, 9, 1500)
fortresses = [Fortress(75, 550, 3), Fortress(298, 550, 3),
              Fortress(521, 550, 3)]

while running:
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if current_menu == 'GAME' and player.alive:
                if event.key == pygame.K_s:
                    player.move_right = True
                elif event.key == pygame.K_a:
                    player.move_left = True
                elif event.key == pygame.K_SPACE:
                    if player.shoot():
                        player_fire_SFX.play()
                elif event.key == pygame.K_ESCAPE:
                    current_menu = 'PAUSED'

        elif event.type == pygame.KEYUP:
            if current_menu == 'GAME':
                if event.key == pygame.K_s:
                    if player.alive:
                        player.move_right = False
                elif event.key == pygame.K_a:
                    if player.alive:
                        player.move_left = False

    # Background
    WIN.fill((0, 0, 0))

    if current_menu == 'HOME':
        draw_text(WIN, SCREEN_WIDTH // 2, 160, "Space Invaders by PlaceHolderHere", WHITE)

        # Buttons
        play_button.blit(WIN)
        controls_button.blit(WIN)

        if play_button.is_clicked():
            current_menu = 'GAME'

        elif controls_button.is_clicked():
            current_menu = 'CONTROLS'

    elif current_menu == 'CONTROLS':
        # Controls
        draw_text(WIN, SCREEN_WIDTH // 2, 224, "Controls:", WHITE)
        draw_text(WIN, SCREEN_WIDTH // 2, 288, "A: Left", WHITE)
        draw_text(WIN, SCREEN_WIDTH // 2, 352, "S: Right", WHITE)
        draw_text(WIN, SCREEN_WIDTH // 2, 416, "Space: Shoot", WHITE)
        draw_text(WIN, SCREEN_WIDTH // 2, 480, "Escape: Pause", WHITE)

        main_menu_button.blit(WIN)
        if main_menu_button.is_clicked():
            current_menu = 'HOME'

    elif current_menu == 'PAUSED':
        main_menu_button.blit(WIN)
        resume_button.blit(WIN)
        restart_button.blit(WIN)
        quit_button.blit(WIN)

        if main_menu_button.is_clicked():
            # Resets Game Variables
            score = 0
            level = 1
            player.lives = 3
            player.reset(30, SCREEN_HEIGHT - 70)
            aliens.reset()
            aliens_move_down = False
            for fortress in fortresses:
                fortress.reset_fortress()
            current_menu = 'HOME'

        elif resume_button.is_clicked():
            current_menu = 'GAME'

        elif restart_button.is_clicked():
            # Resets Game Variables
            score = 0
            level = 1
            player.lives = 3
            player.reset(30, SCREEN_HEIGHT - 70)
            aliens.reset()
            aliens_move_down = False
            for fortress in fortresses:
                fortress.reset_fortress()
            current_menu = 'GAME'

        elif quit_button.is_clicked():
            running = False
            break

    elif current_menu == 'DEAD':
        draw_text(WIN, SCREEN_WIDTH // 2, 220, "GAME OVER", RED)
        draw_text(WIN, SCREEN_WIDTH // 2, 280, f"Final Score: {score}", WHITE)

        # Buttons
        main_menu_defeat_button.blit(WIN)
        retry_Button.blit(WIN)
        if main_menu_defeat_button.is_clicked():
            # Resets Game Variables
            score = 0
            level = 1
            player.lives = 3
            player.reset(30, SCREEN_HEIGHT - 70)
            aliens.reset()
            aliens_move_down = False
            for fortress in fortresses:
                fortress.reset_fortress()
            current_menu = 'HOME'
        elif retry_Button.is_clicked():
            # Resets Game Variables
            score = 0
            level = 1
            player.lives = 3
            player.reset(30, SCREEN_HEIGHT - 70)
            aliens.reset()
            aliens_move_down = False
            for fortress in fortresses:
                fortress.reset_fortress()
            current_menu = 'GAME'

    elif current_menu == 'GAME':
        # HUD
        draw_text(WIN, SCREEN_WIDTH // 2, 40, score, WHITE)
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

        elif player.respawning:
            player.respawning = False
            player.reset(30, SCREEN_HEIGHT - 70)

        if new_level_animation_cooldown > 0:
            new_level_animation_cooldown -= 1
            new_level_animation_counter += 1
            if new_level_animation_counter > 10:
                new_level_animation_counter = 0
                new_level_blit_animation = not new_level_blit_animation

            if new_level_blit_animation:
                player.blit(WIN)
                aliens.blit(WIN)
                for fort in fortresses:
                    fort.blit(WIN)

        # Player Processing
        else:
            if player.alive:
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
                                        alien_death_SFX.play()
                                        if player.bullets:
                                            player.bullets.pop(bullet_index)
                                            break

                        # Fortress Collisions
                        for fort in fortresses:
                            fort_shape = fort.shape
                            if bullet.is_colliding(fort.get_fortress_rect()):
                                # Calculating Bullet Range for collisions with the shape
                                lower_bullet_x_range = get_lower_bound(fort.x, bullet.x, fort.rect_size)
                                upper_bullet_x_range = get_upper_bound(fort.x, bullet.x + bullet.size_x, fort.rect_size,
                                                                       fort.num_cols)

                                # Blast Collisions
                                collision_detected = False
                                for row_index in range(fort.num_rows - 1, 0, -1):
                                    if collision_detected:
                                        break
                                    else:
                                        for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                                            if fort_shape[row_index][col_index] == '1':
                                                collide_block_x = fort.x + (col_index * fort.rect_size)
                                                collide_block_y = fort.y + (row_index * fort.rect_size)
                                                collide_block_rect = pygame.Rect(collide_block_x, collide_block_y,
                                                                                 fort.rect_size, fort.rect_size)
                                                if bullet.is_colliding(collide_block_rect):
                                                    # Calculations for blast radius
                                                    blast_x = collide_block_x - bullet.blast_radius  # Left
                                                    blast_y = collide_block_y - bullet.blast_radius  # Top
                                                    blast_size_x = blast_x - fort.x
                                                    blast_size_y = blast_y - fort.y

                                                    # Blast Ranges
                                                    blast_lower_x_range = max(0, blast_size_x // fort.rect_size)
                                                    blast_upper_x_range = min(fort.num_cols, (
                                                        blast_size_x + (2 * bullet.blast_radius)) // fort.rect_size + 1)

                                                    blast_lower_y_range = max(0, blast_size_y // fort.rect_size)
                                                    blast_upper_y_range = min(fort.num_rows, (blast_size_y + (
                                                                2 * bullet.blast_radius)) // fort.rect_size + 1)

                                                    blast_x_range = range(blast_lower_x_range, blast_upper_x_range)
                                                    blast_y_range = range(blast_lower_y_range, blast_upper_y_range)

                                                    # Blast Radius Collisions
                                                    for blast_row_index in blast_y_range:
                                                        for blast_col_index in blast_x_range:
                                                            if fort_shape[blast_row_index][blast_col_index] == '1':
                                                                x = fort.x + (blast_col_index * fort.rect_size)
                                                                y = fort.y + (blast_row_index * fort.rect_size)
                                                                if bullet.blast_calculation(collide_block_x,
                                                                                            collide_block_y, x, y,
                                                                                            fort.rect_size):
                                                                    fort_shape[blast_row_index][blast_col_index] = '0'

                                                    # Disabling all collision checks related to this bullet
                                                    collision_detected = True
                                                    if player.bullets:
                                                        player.bullets.pop(bullet_index)
                                                    break
            else:
                if player.lives > 0:
                    aliens.clear_bullets()
                    player.alive = True
                    player.respawning = True
                    player.respawn_cooldown = 120
                    player.lives -= 1
                else:
                    current_menu = 'DEAD'

            # Level Reset
            if aliens.num_alive_aliens <= 0:
                player.bullets = []
                new_level_animation_cooldown = 120
                level += 1
                aliens.global_firing_chance = max(MIN_ALIEN_FIRING_CHANCE,
                                                  aliens.global_firing_chance - (level * 10))
                aliens.movement_trigger = max(MIN_ALIEN_MOVEMENT_TRIGGER,
                                              aliens.movement_trigger - ((level // 5) * 5))
                aliens.reset()
                # Fortress Reset
                for fortress in fortresses:
                    fortress.reset_fortress()

            # Alien Processing
            if aliens_move_down:
                aliens_move_down = False
                aliens.move_down()

            for alien_row_index, row in enumerate(aliens.alien_rows):
                for alien in row.aliens:
                    if alien.alive:
                        if alien.y > player.y:
                            current_menu = 'DEAD'

                        if alien_row_index == 0:
                            # Border Collisions
                            if alien.x + alien.size_x > SCREEN_WIDTH - 30:
                                aliens_move_down = True
                            elif alien.x < 30:
                                aliens_move_down = True

                        # Alien Firing
                        if not alien.bullet_fired:
                            num_dead_aliens = aliens.TOTAL_NUM_ALIENS - aliens.num_alive_aliens
                            firing_chance = max(MIN_ALIEN_FIRING_CHANCE,
                                                aliens.global_firing_chance - (num_dead_aliens * 5))
                            if random.randint(0, firing_chance) == 0:
                                alien.shoot()

                    # Alien bullet processing
                    if alien.bullet_fired:
                        if alien.bullet.y > SCREEN_HEIGHT:  # checks if bullet flew off screen
                            alien.bullet_fired = False
                        else:
                            # Player Collisions
                            if alien.bullet.is_colliding(player.get_rect()):
                                player.alive = False
                                alien.bullet_fired = False
                                player_death_SFX.play()

                            # Fortress Collisions
                            for fort in fortresses:
                                fort_shape = fort.shape
                                if alien.bullet.is_colliding(fort.get_fortress_rect()):
                                    # Calculating Bullet Range for collisions with the shape
                                    collision_size_x = alien.bullet.x - fort.x
                                    lower_bullet_x_range = max(0, collision_size_x // fort.rect_size)
                                    upper_bullet_x_range = min(fort.num_cols, (
                                                collision_size_x + alien.bullet.size_x) // fort.rect_size + 1)

                                    # Blast Collisions
                                    collision_detected = False
                                    for row_index in range(fort.num_rows - 1, 0, -1):
                                        if collision_detected:
                                            break
                                        else:
                                            for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                                                if fort.shape[row_index][col_index] == '1':
                                                    collide_block_x = fort.x + (col_index * fort.rect_size)
                                                    collide_block_y = fort.y + (row_index * fort.rect_size)
                                                    collide_rect = pygame.Rect(collide_block_x, collide_block_y,
                                                                               fort.rect_size, fort.rect_size)
                                                    if alien.bullet.is_colliding(collide_rect):
                                                        # Calculations for blast radius
                                                        # Top Left Coordinates for Blast Radius hit box
                                                        blast_x = collide_block_x - alien.bullet.blast_radius
                                                        blast_y = collide_block_y - alien.bullet.blast_radius
                                                        blast_size_x = blast_x - fort.x
                                                        blast_size_y = blast_y - fort.y

                                                        # Blast Ranges
                                                        blast_lower_x_range = max(0, blast_size_x // fort.rect_size)
                                                        blast_upper_x_range = min(fort.num_cols, (blast_size_x + (
                                                                    2 * alien.bullet.blast_radius)) //
                                                                                  fort.rect_size + 1)

                                                        blast_lower_y_range = max(0, blast_size_y // fort.rect_size)
                                                        blast_upper_y_range = min(fort.num_rows, (blast_size_y + (
                                                                    2 * alien.bullet.blast_radius)) //
                                                                                  fort.rect_size + 1)

                                                        blast_x_range = range(blast_lower_x_range,
                                                                              blast_upper_x_range)
                                                        blast_y_range = range(blast_lower_y_range,
                                                                              blast_upper_y_range)

                                                        # Blast Radius Collisions
                                                        for blast_row_index in blast_y_range:
                                                            for blast_col_index in blast_x_range:
                                                                if fort_shape[blast_row_index][
                                                                        blast_col_index] == '1':
                                                                    x = fort.x + (
                                                                                blast_col_index * fort.rect_size)
                                                                    y = fort.y + (
                                                                                blast_row_index * fort.rect_size)
                                                                    if alien.bullet.blast_calculation(
                                                                            collide_block_x, collide_block_y, x, y,
                                                                            fort.rect_size):
                                                                        fort_shape[blast_row_index][
                                                                            blast_col_index] = 0

                                                        # Disabling further collision checks
                                                        alien.bullet_fired = False
                                                        collision_detected = True
                                                        break

                        alien.bullet.move()
                        alien.bullet.blit(WIN)

            # Alien Rendering
            aliens.blit(WIN)

            # Fortresses Blit
            for fortress in fortresses:
                fortress.blit(WIN)

    pygame.display.update()
