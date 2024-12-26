import pygame
from os.path import join
from random import randint, uniform

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 350

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

# Star Class
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surface) -> None:
        super().__init__(groups)
        self.image = star_surface
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

# Meteor Class
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.speed = randint(50, 100)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 2000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

# Laser Class
class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom = position)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt

        if self.rect.bottom < 0:
            self.kill()

# General Setup
pygame.init() # Initialize Pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the Title
pygame.display.set_caption('Space Shooter')

# Import Sprite Surfaces
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surface = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join('images','laser.png')).convert_alpha()

running = True

clock = pygame.time.Clock() 

# Surface
surface = pygame.Surface((100, 200))
surface.fill('orange')
x = 100

# Group
all_sprites = pygame.sprite.Group()

# Stars
stars = [Star(all_sprites, star_surface) for _ in range(20)]

# Meteor

# Player
player = Player(all_sprites)

# Custom Event for Meteor
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


# Game Loop
while running:
    # Delta Time
    dt = clock.tick() / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, (randint(0, WINDOW_WIDTH), 0), all_sprites)

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
