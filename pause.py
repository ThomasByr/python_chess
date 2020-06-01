import pygame

from button import Button

pygame.font.init()
myfont = pygame.font.SysFont("JetBrains Mono Regular", 20)


class Pause(Button):
    def __init__(self, game):
        """
        classe pour le bouton "pause"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 3
        self.game = game

        self.get_image(self.action)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect.x = 550
        self.rect.y = 475

    def click(self):
        self.game.pause = True
        # sauvegarde de la durée de jeu passée
        self.game.new_start = self.game.clock.get_time_in_sec()

        textsurface = myfont.render(
            "en pause...", True, self.game.data["pause_text_indicator_color"]
        )
        self.game.screen.blit(textsurface, (580, 480))
