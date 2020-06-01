import pygame
from board import Board
from player import Player


class Human(Player):
    def __init__(self, color: str):
        """
        une classe pour les joueurs humains

        Parameters
        ----------
            color : str
                la couleur des pièces du joueur
        """
        super().__init__()
        self.name = f"human{color}"
        self.color = color
        self.check = False

    def click_tests(self, game, index: tuple({int})):
        """
        tests de clics lorsque le joueur humain joue

        Parameters
        ----------
            game : Game
                le jeu
            index : tuple
                les coordonnées du clic
        """

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
                        piece.move_to(game, from_index, index)
                        game.board.deselect_all()
                        game.next_player()  # joueur suivant

            piece = game.board.board[index]
            if piece is not None and piece.color == game.cur_player.color:
                game.board.deselect_all()
                piece.click(game, index)
