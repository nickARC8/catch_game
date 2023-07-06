import pygame
import random

# Background
background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (800, 600))

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Player dimensions and movement variables
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Obstacle dimensions and movement variables
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 3

# Power-up dimensions and effect variables
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
POWERUP_EFFECT_DURATION = 200  # In frames

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Parkour Game")

clock = pygame.time.Clock()

# Load game sounds
collision_sound = pygame.mixer.Sound("collision.wav")
powerup_sound = pygame.mixer.Sound("powerup.wav")

# Load game images
player_img = pygame.image.load("player.png").convert_alpha()
obstacle_img = pygame.image.load("obstacle.png").convert_alpha()
powerup_img = pygame.image.load("powerup.png").convert_alpha()

# Resize game images
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
powerup_img = pygame.transform.scale(powerup_img, (POWERUP_WIDTH, POWERUP_HEIGHT))

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH // 2
        self.rect.y = WINDOW_HEIGHT - PLAYER_HEIGHT
        self.score = 0
        self.powerup_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Prevent player from moving out of the window boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WINDOW_WIDTH - PLAYER_WIDTH:
            self.rect.x = WINDOW_WIDTH - PLAYER_WIDTH

        # Update power-up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.deactivate_powerup()

    def activate_powerup(self):
        global running
        self.powerup_timer = POWERUP_EFFECT_DURATION
        running = False

    def deactivate_powerup(self):
        self.image = player_img

# Define the Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += OBSTACLE_SPEED

# Define the Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += OBSTACLE_SPEED

# Create sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Game variables
level = 1
score_needed_for_powerup = 100

# Game loop
running = True
while running:
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate obstacles
    if random.randint(0, 30) < (level * 2.5):
        obstacle_x = random.randint(0, WINDOW_WIDTH - OBSTACLE_WIDTH)
        obstacle = Obstacle(obstacle_x, -OBSTACLE_HEIGHT)
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Generate power-ups
    if random.randint(0, 300) < 4:
        powerup_x = random.randint(0, WINDOW_WIDTH - POWERUP_WIDTH)
        powerup = PowerUp(powerup_x, -POWERUP_HEIGHT)
        all_sprites.add(powerup)
        powerups.add(powerup)

    # Update sprites
    all_sprites.update()

    # Check for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacles, False):
        collision_sound.play()
        running = False

    # Check for collisions between player and power-ups
    powerup_collisions = pygame.sprite.spritecollide(player, powerups, True)
    if powerup_collisions:
        powerup_sound.play()
        player.score += len(powerup_collisions)
        if player.score >= score_needed_for_powerup:
            player.activate_powerup()
            player.score = 0


    # Draw sprites
    all_sprites.draw(window)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
