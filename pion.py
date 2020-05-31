from piece import Piece
import pygame


class Pion(Piece):
    def __init__(self, color: str):
        """
        une classe pour la pièce [pion]

        Parameters
        ----------
            color : str
                la couleur de la pièce : "n" ou "b"
        """
        super().__init__()

        self.name = "pion"
        self.color = color
        self.value = 1.0

        self.get_image(self.name, self.color)

    def accessible(self, board, index: tuple({int})) -> set({tuple({int})}):
        """
        donne les cases accessibles par [roi]

        Parameters
        ----------
            boad : np.array
                le tableau de jeu
            index : tuple
                la position de la pièce sélectionnée
        Returns
        -------
            set : le set des positions accessibles
        """
        res = set()

        # si le pion est blanc
        if self.color == "b":
            if (
                index[0] == 6
                and index[0] - 2 >= 0
                and board[index[0] - 2, index[1]] is None
            ):
                res.add((index[0] - 2, index[1]))

            if index[0] - 1 >= 0 and board[index[0] - 1, index[1]] is None:
                res.add((index[0] - 1, index[1]))

            if (
                index[0] - 1 >= 0
                and index[1] + 1 <= 7
                and board[index[0] - 1, index[1] + 1] is not None
            ):
                res.add((index[0] - 1, index[1] + 1))

            if (
                index[0] - 1 >= 0
                and index[1] - 1 >= 0
                and board[index[0] - 1, index[1] - 1] is not None
            ):
                res.add((index[0] - 1, index[1] - 1))

        # si le pion est noir
        if self.color == "n":
            if (
                index[0] == 1
                and index[0] + 2 <= 7
                and board[index[0] + 2, index[1]] is None
            ):
                res.add((index[0] + 2, index[1]))

            if index[0] + 1 <= 7 and board[index[0] + 1, index[1]] is None:
                res.add((index[0] + 1, index[1]))

            if (
                index[0] + 1 <= 7
                and index[1] + 1 <= 7
                and board[index[0] + 1, index[1] + 1] is not None
            ):
                res.add((index[0] + 1, index[1] + 1))

            if (
                index[0] + 1 <= 7
                and index[1] - 1 >= 0
                and board[index[0] + 1, index[1] - 1] is not None
            ):
                res.add((index[0] + 1, index[1] - 1))

        return res  # todo: ajouter "en passant"
