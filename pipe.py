import pygame, random
from ui import resource_path

class Pipe(pygame.sprite.Sprite):  
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen
        self.load(x, y)
    def get(self) :
        return pygame.image.load(resource_path("sprites/pipe-green.png"))
    def load(self, x, y) :
        self.speed, self.x, self.y = 2, x, y 
        self.image = self.get()
        height = random.randint(180, 480)
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), height))
        self.rect = pygame.Rect(x, y, self.image.get_width(), height)
        self.rect.center = [x, y]
        self.scored = False
    def update(self) :
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.load(287, self.y)

class PipeDown(Pipe) :
    def get(self):
            img = super().get()
            return pygame.transform.flip(img, False, True)
