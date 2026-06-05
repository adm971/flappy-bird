import pygame
pygame.init()


class Timer:
    def __init__(self, seconds):# Durée du timer en secondes
        self.seconds = seconds # Temps au moment de la création du timer 
        self.ticks = pygame.time.get_ticks() # Heure à laquelle le timer doit déclencher l'action 
        self.time = self.ticks + seconds * 1000 # Indicateur que le timer a déclenché l'action
        self.cooldown = False

    def wait(self, action): # Vérifie si le temps est écoulé et que l'action n'a pas encore été déclenchée
        if not self.cooldown and pygame.time.get_ticks() >= self.time:  
            self.cooldown = True
            print("Le compte à rebours a atteint :", self.time)
            print("Durée initiale (secondes) :", self.seconds)
            print("Temps de départ (ticks) :", self.ticks)
            action() # Exécuter l'action passée en lambda



