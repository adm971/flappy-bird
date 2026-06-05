import pygame, os, sys 
from datetime import datetime
pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Score : 
    def __init__(self, score) :
        self.score = int(score) 
        self.file = "scores.txt"
        self.get_point = pygame.mixer.Sound(resource_path("audio/point.ogg"))
        self.scored = False
    def save(self) :
        if not os.path.exists(self.file) :
            self.best_score = 0
            with open(self.file, "w") as file :
                file.write(str(self.best_score))
        else :
                with open(self.file, "r") as file :
                    self.best_score = int(file.read())
        if self.score > self.best_score : 
            self.best_score = self.score
            with open(self.file, "w") as file : 
                file.write(str(self.best_score))
            self.score = 0 

class Background : 
    def __init__(self):
        hour = datetime.now().hour
        if 7 <= hour < 20:
            self.image = pygame.image.load(resource_path("sprites/background-day.png"))
        else:
            self.image = pygame.image.load(resource_path("sprites/background-night.png"))


class Title(pygame.sprite.Sprite) : 
    def __init__(self, screen, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource_path("sprites/message.png"))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen = screen 