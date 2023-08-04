import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Move, Shoot, Blow Out, and Random Movement")

# Square position and size
square_size = 50
square_x = (screen_width - square_size) // 2
square_y = (screen_height - square_size) // 2
square_health = 100  # Initial health value

# Enemy properties
num_enemies = 3
enemy_size = 50
enemy_speed = 2
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(0, screen_width - enemy_size)
    enemy_y = random.randint(0, screen_height - enemy_size)
    enemies.append({"x": enemy_x, "y": enemy_y, "health": 100, "color": red, "direction": [random.choice([-1, 1]), random.choice([-1, 1])]})

# Bullet properties
bullet_width = 10
bullet_height = 5
bullet_speed = 10
bullets = []

# Player missile properties
missile_width = 10
missile_height = 5
missile_speed = 15
player_missiles = []

# Enemy bullet properties
enemy_bullet_width = 10
enemy_bullet_height = 5
enemy_bullet_speed = 5
enemy_bullets = []

# Square movement speed
move_speed = 5

# Health bar dimensions
health_bar_width = 50
health_bar_height = 10

# Game over flag
game_over = False

# Item box properties
item_box_size = 30
item_box_color = (255, 255, 0)  # Yellow
item_box_x = random.randint(0, screen_width - item_box_size)
item_box_y = random.randint(0, screen_height - item_box_size)
item_box_collected = False

# Player missile tracking flag
enable_tracking = False

# Bullet color for the player
bullet_color = black  # Default bullet color

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for space bar press to shoot
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            bullet_x = square_x + square_size  # Start the bullet at the player's position
            bullet_y = square_y + square_size // 2
            bullets.append([bullet_x, bullet_y])

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Update square position based on keyboard input
    if keys[pygame.K_LEFT] and square_x > 0:
        square_x -= move_speed
    if keys[pygame.K_RIGHT] and square_x < screen_width - square_size:
        square_x += move_speed
    if keys[pygame.K_UP] and square_y > 0:
        square_y -= move_speed
    if keys[pygame.K_DOWN] and square_y < screen_height - square_size:
        square_y += move_speed

    # Update bullet positions
    for bullet in bullets:
        bullet[0] += bullet_speed

    # Update player missiles and tracking
    for missile in player_missiles:
        missile[0] += missile_speed

        if enable_tracking:
            target_enemy = None
            min_distance = float("inf")

            for enemy in enemies:
                enemy_center_x = enemy["x"] + enemy_size / 2
                enemy_center_y = enemy["y"] + enemy_size / 2
                distance = ((missile[0] - enemy_center_x) ** 2 + (missile[1] - enemy_center_y) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    target_enemy = enemy

            if target_enemy:
                enemy_center_x = target_enemy["x"] + enemy_size / 2
                enemy_center_y = target_enemy["y"] + enemy_size / 2
                angle = math.atan2(enemy_center_y - missile[1], enemy_center_x - missile[0])
                missile[0] += missile_speed * math.cos(angle)
                missile[1] += missile_speed * math.sin(angle)

    # Check for collision between player and item box
    if not item_box_collected:
        item_box_rect = pygame.Rect(item_box_x, item_box_y, item_box_size, item_box_size)
        player_rect = pygame.Rect(square_x, square_y, square_size, square_size)
        if item_box_rect.colliderect(player_rect):
            item_box_collected = True
            enable_tracking = True  # Enable tracking for player's missiles
            bullet_color = red  # Change the player's bullet color to red

    # Update enemy bullets
    for bullet in enemy_bullets:
        bullet[0] -= enemy_bullet_speed

    # Update enemies
    for enemy in enemies:
        if enemy["x"] <= 0 or enemy["x"] >= screen_width - enemy_size:
            enemy["direction"][0] *= -1
        if enemy["y"] <= 0 or enemy["y"] >= screen_height - enemy_size:
            enemy["direction"][1] *= -1
        enemy["x"] += enemy_speed * enemy["direction"][0]
        enemy["y"] += enemy_speed * enemy["direction"][1]

    # Check for collision between player bullets and enemies
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemy["health"] -= 10

                if enemy["health"] <= 0:
                    enemy["color"] = blue  # Turn the enemy blue when defeated

    # Check for collision between enemy bullets and the player
    for bullet in enemy_bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height)
        player_rect = pygame.Rect(square_x, square_y, square_size, square_size)
        if bullet_rect.colliderect(player_rect):
            enemy_bullets.remove(bullet)
            square_health -= 10

    # Check for game over conditions
    if square_health <= 0:
        game_over = True
        game_over_text = "Game Over"
    elif all(enemy["color"] == blue for enemy in enemies):
        game_over = True
        game_over_text = "You Win"

    # Fill the screen with white color
    screen.fill(white)

    # Draw the square
    pygame.draw.rect(screen, black, (square_x, square_y, square_size, square_size))

    # Draw square health bar
    health_bar_x = square_x
    health_bar_y = square_y - health_bar_height - 5
    pygame.draw.rect(screen, green, (health_bar_x, health_bar_y, health_bar_width * (square_health / 100), health_bar_height))

    # Draw enemies and their health bars
    for enemy in enemies:
        pygame.draw.rect(screen, enemy["color"], (enemy["x"], enemy["y"], enemy_size, enemy_size))
        health_bar_x = enemy["x"]
        health_bar_y = enemy["y"] - health_bar_height - 5
        pygame.draw.rect(screen, green, (health_bar_x, health_bar_y, health_bar_width * (enemy["health"] / 100), health_bar_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw player missiles
    for missile in player_missiles:
        pygame.draw.rect(screen, missile_color, (missile[0], missile[1], missile_width, missile_height))

    # Draw enemy bullets
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, enemy_bullet_color, (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))

    # Draw item box if not collected
    if not item_box_collected:
        pygame.draw.rect(screen, item_box_color, (item_box_x, item_box_y, item_box_size, item_box_size))

    # Display game over message
    if game_over:
        font = pygame.font.Font(None, 36)
        game_over_text_surface = font.render(game_over_text, True, red)
        game_over_rect = game_over_text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text_surface, game_over_rect)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
