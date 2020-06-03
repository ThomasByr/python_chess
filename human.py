import pygame
from board import Board
from player import Player


class Human(Player):
    def __init__(self, color: str, game):
        """
        une classe pour les joueurs humains

        Parameters
        ----------
            color : str
                la couleur des pièces du joueur
            game : Game
        """
        super().__init__()
        self.name = f"human{color}"
        self.color = color
        self.check = False
        self.game = game

    def click_tests(self, index: tuple({int})):
        """
        tests de clics lorsque le joueur humain joue

        Parameters
        ----------
            game : Game
                le jeu
            index : tuple
                les coordonnées du clic
        """
        game = self.game

        # clic en dehors du plateau
        if index[1] >= 8:
            game.board.deselect_all()

        # clic sur le plateau
        else:
            from_index = game.board.get_selected()
            if from_index is not None:  # si on a déjà sélectionné une pièce
                piece = game.board.board[from_index]
                if piece is not None:  # si ce qui a été sélectionné est bien une pièce
                    if index in piece.viable:  # si le déplacement est viable
                        # déplacer la pièce
                        piece.move_to(game, game.board.board, from_index, index)
                        game.next_player()  # joueur suivant

            piece = game.board.board[index]
            game.board.deselect_all()
            # clic sur une autre pièce de sa couleur
            if piece is not None and piece.color == game.cur_player.color:
                piece.click(game, index)
