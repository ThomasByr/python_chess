from piece import Piece
import pygame


class Cavalier(Piece):
    def __init__(self, color: str, load: bool = True):
        """
        une classe pour la pièce [cavalier]

        Parameters
        ----------
            color : str
                la couleur de la pièce : "n" ou "b"
        """
        super().__init__()

        self.name = "cavalier"
        self.color = color
        self.value = 3.2

        if load:
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

        res.add((index[0] + 2, index[1] + 1))
        res.add((index[0] + 2, index[1] - 1))
        res.add((index[0] - 2, index[1] + 1))
        res.add((index[0] - 2, index[1] - 1))

        res.add((index[0] + 1, index[1] + 2))
        res.add((index[0] + 1, index[1] - 2))
        res.add((index[0] - 1, index[1] + 2))
        res.add((index[0] - 1, index[1] - 2))

        return res
