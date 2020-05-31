import pygame

from button import Button


class Undo(Button):
    def __init__(self, game):
        """
        classe pour le bouton "undo"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 1

        self.get_image(self.action)
        self.rect.x = 750
        self.rect.y = 480

        self.game = game

    def click(self):
        print("boutont 1 activé !")
        print("fonctionnalité désactivée")
