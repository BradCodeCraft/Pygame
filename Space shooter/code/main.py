import pygame
from os.path import join
from random import randint


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if recent_keys[pygame.K_SPACE]:
            print("fire laser")

# Star Class
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surface) -> None:
        super().__init__(groups)
        self.image = star_surface
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


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

# Group
all_sprites = pygame.sprite.Group()
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
stars = [Star(all_sprites, star_surface) for _ in range(20)]
player = Player(all_sprites)

# Import Images
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

    # Update All Sprites
    all_sprites.update(dt)

    # Draw Game
    display_surface.fill('black')
    
    # Draw Meteor
    # display_surface.blit(meteor_surface, meteor_rect)
    
    # Draw Laser
    # display_surface.blit(laser_surface, laser_rect)

    # Draw Player
    all_sprites.draw(display_surface)

    # Move Player
    pygame.display.update() # Update Display

pygame.quit() # Quit Pygame
