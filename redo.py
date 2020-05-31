import pygame

from button import Button


class Redo(Button):
    def __init__(self, game):
        """
        classe pour le bouton "redo"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 2

        self.get_image(self.action)
        self.rect.x = 780
        self.rect.y = 480

        self.game = game

    def click(self):
        print("boutont 2 activé !")
        print("fonctionnalité désactivée")
