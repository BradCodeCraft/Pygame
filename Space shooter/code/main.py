import pygame
from os.path import join
from random import randint

# General Setup
pygame.init() # Initialize Pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the Title
pygame.display.set_caption('Space Shooter')

running = True

clock = pygame.time.Clock() 

# Surface
surface = pygame.Surface((100, 200))
surface.fill('orange')
x = 100

# Import Images
player_surface = pygame.image.load(join('images', 'player.png')).convert_alpha() # Only works if the command to execute the script is in the main directory (i.e. space shooter)
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2(20, -20)
player_speed = 10

star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH - 100), randint(0, WINDOW_HEIGHT - 100)) for _ in range(20)]

meteor_surface = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# Game Loop
while running:
    # Delta Time
    dt = clock.tick() / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw Game
    display_surface.fill('black')

    # Draw Meteor
    display_surface.blit(meteor_surface, meteor_rect)
    
    # Draw Laser
    display_surface.blit(laser_surface, laser_rect)
    
    # Draw Stars
    for i in range(20):
        display_surface.blit(star_surface, star_positions[i])

    # Draw Player
    display_surface.blit(player_surface, player_rect)

    # Bound Player like Dvd Logo
    if player_rect.top <= 0 or player_rect.bottom >= WINDOW_HEIGHT:
        player_direction.y *= -1
    if player_rect.left <= 0 or player_rect.right >= WINDOW_WIDTH:
        player_direction.x *= -1

    # Move Player
    player_rect.center += player_direction * player_speed * dt

    pygame.display.update() # Update Display

pygame.quit() # Quit Pygame
