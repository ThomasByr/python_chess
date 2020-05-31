import pygame
from player import Player


class Ai(Player):
    def __init__(self, color: str):
        """
        une classe pour l'ordinateur

        Parameters
        ----------
            color : str
                la couleur des pièces
        """
        super().__init__()
        self.name = f"ai{color}"
        self.color = color
        self.check = False

    def play(self, game):
        """
        permet à l'ordinateur de jouer son tour

        Parameters
        ----------
            game : Game
                l'instance du jeu      
        """
        print("tour de l'ia à venir...")
        game.next_player()
