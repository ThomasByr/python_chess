import pygame
import time

from button import Button

pygame.font.init()
myfont = pygame.font.SysFont("JetBrains Mono Regular", 20)


class Play(Button):
    def __init__(self, game):
        """
        classe pour le bouton "play"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 4
        self.game = game

        self.get_image(self.action)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect.x = 550
        self.rect.y = 475

    def click(self):
        self.game.pause = False
        self.game.clock.reset(self.game.new_start)

        t = 3  # temps avant reprise en secondes
        while t > 0:
            pygame.draw.rect(
                self.game.screen,
                self.game.data["background_color"],
                (580, 480, 100, 20),
            )
            textsurface = myfont.render(
                f"reprise dans {t}...",
                True,
                self.game.data["play_text_indicator_color"],
            )
            self.game.screen.blit(textsurface, (580, 480))
            pygame.display.flip()
            t -= 1
            time.sleep(1)
