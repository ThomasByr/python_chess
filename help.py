import pygame

from button import Button


class Help(Button):
    def __init__(self, game):
        """
        une classe pour le bouton "help"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 1
        self.game = game

        self.get_image(self.action)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect.x = 775
        self.rect.y = 475

    def click(self):
        print("boutont 1 activé !")
        print("fonctionnalité désactivée")
