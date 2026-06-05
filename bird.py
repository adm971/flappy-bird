import pygame, sys, os, subprocess
from ui import resource_path
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2)
pygame.init()

def animate(frames, index, speed) :
    index += speed 
    if index >= len(frames) : 
        index = 0 
    return frames[int(index)], index

class Bird(pygame.sprite.Sprite) :
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load(resource_path("sprites/bluebird-upflap.png")),pygame.image.load(resource_path("sprites/bluebird-midflap.png")),
        pygame.image.load(resource_path("sprites/bluebird-downflap.png"))]
        self.image = pygame.image.load(resource_path("sprites/bluebird-midflap.png"))
        self.frame_index, self.animation_speed = 0, 0.15
        self.rect = self.image.get_rect()
        self.screen, self.x, self.y = screen, x, y
        self.rect.center = [x, y]
        self.gravity, self.velocity = 0.25, 0 
        self.swoosh, self.die, self.hit = pygame.mixer.Sound(resource_path("audio/swoosh.ogg")), pygame.mixer.Sound(resource_path("audio/die.ogg")), pygame.mixer.Sound(resource_path("audio/hit.ogg"))
        self.last_jump, self.jump_delay, self.is_alive = pygame.time.get_ticks(), 2000, True
    def update(self) :
        self.image, self.frame_index = animate(self.frames, self.frame_index, self.animation_speed)
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top > 512 :
            self.is_alive = False
            self.die.play()
        if self.rect.top < 0 :
            self.rect.top, self.velocity = 1, 0 
        keys = pygame.mouse.get_pressed()
        if keys[0] :  
                self.velocity = -2
                self.swoosh.play()