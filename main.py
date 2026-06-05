import pygame, sys, os
from ui import Background, Title, Score, resource_path
from pipe import Pipe, PipeDown
from bird import Bird
from timer import Timer

Flappyfont = pygame.font.Font(resource_path("flappyfont.ttf"), 30)

class Game :

    def Text(self, font_name, size, text, position, color, screen):
        
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)  # True = antialiasing
        text_rect = text_surface.get_rect()
        text_rect.center = position  # Placer le texte à la position donnée (x, y)
        self.screen = screen 
        self.screen.blit(text_surface, text_rect)
  

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((288, 512))
        pygame.display.set_caption("Flappy bird")
        self.clock = pygame.time.Clock()
        self.start, self.rungame, self.lose = True, False, False 

        icon = pygame.image.load(resource_path("favicon.ico"))
        pygame.display.set_icon(icon)

        self.background = Background()

        self.title = Title(self.screen, 288 / 2, 512 / 2)
        self.title_group = pygame.sprite.Group()
        self.title_group.add(self.title)

        self.gameover = Title(self.screen, 288 / 2, 512 / 2)
        self.gameover.image = pygame.image.load(resource_path("sprites/gameover.png"))
        self.gameover_group = pygame.sprite.Group()
        self.gameover_group.add(self.gameover)

        self.score = Score(0)
        self.score.save()
        print("j'écris depuis main et best score = ", self.score.best_score)

        self.bird = Bird(288 / 2, 200, self.screen)
        self.bird_group = pygame.sprite.Group()
        self.bird_group.add(self.bird)
        

        self.pipe = Pipe(288, 512, self.screen)
        self.pipedown = PipeDown(288, 0, self.screen)
        self.pipe_group = pygame.sprite.Group()
        self.pipedown_group = pygame.sprite.Group()
        self.pipe_group.add(self.pipe)
        self.pipedown_group.add(self.pipedown)


    def run(self) : # Ecran titre
        while self.start :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.screen.blit(self.background.image, (0, 0))
                self.title_group.draw(self.screen)
                if event.type == pygame.MOUSEBUTTONDOWN : 
                    if event.button == 3 :
                        self.score.get_point.play()
                        self.title.kill()
                        self.rungame, self.start = True, False      
            pygame.display.flip()
        self.main_loop() 

    def main_loop(self): # Jeu en cours
        while self.rungame:
            self.screen.blit(self.background.image, (0, 0))

            self.bird_group.update()
            self.bird_group.draw(self.screen)
            self.pipe_group.update()
            self.pipe_group.draw(self.screen)
            self.pipedown_group.update()
            self.pipedown_group.draw(self.screen)

            self.Text("flappyfont.ttf", 30, str(self.score.score), (288 / 2, 30), (0, 0, 0), self.screen)

            self.clock.tick(60)

            if self.bird.is_alive == False :
                self.rungame = False
                self.lose = True

            if hasattr(self, 'timer') and not self.timer.cooldown:
                self.timer.wait(lambda: setattr(self.bird, 'is_alive', False))

            pygame.display.flip()

            for self.pipe in self.pipe_group:
                if not self.pipe.scored and self.pipe.rect.right < self.bird.rect.left:
                    self.score.score += 1 
                    self.pipe.scored = True
                    self.score.get_point.play()

            for bird in self.bird_group :
                if bird.rect.colliderect(self.pipe.rect) or bird.rect.colliderect(self.pipedown.rect) :
                    self.bird.hit.play()
                    self.bird.velocity, self.bird.gravity, self.pipe.speed, self.pipedown.speed = 0, 0, 0, 0
                    # Lance le timer pour la première fois
                    if not hasattr(self, 'timer') :
                        self.timer = Timer(0.5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 3 :
                        self.rungame, self.lose = False, True 

        self.end()

    def end(self) : # Game over
        while self.lose:
            self.score.save()
            self.screen.blit(self.background.image, (0, 0))
            self.gameover_group.draw(self.screen)
            self.Text("flappyfont.ttf", 30, str(self.score.score), (288 / 2, 30), (0, 0, 0), self.screen)
            self.Text("flappyfont.ttf", 30, str(self.score.best_score), (288 / 2, 60), (0, 0, 0), self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 3 :
                        self.lose = False
        Game().run()

if __name__ == "__main__":
    Game().run()
    # pyinstaller --onefile --noconsole main.py
    # pyinstaller --onefile --windowed --icon=favicon.ico --add-data "flappyfont.ttf;." main.py
    # pyinstaller --onefile --windowed --icon=favicon.ico --add-data "sprites;sprites" --add-data "audio;audio" --add-data "flappyfont.ttf;." --add-data "favicon.ico;." main.py