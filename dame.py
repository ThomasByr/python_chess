from piece import Piece
import pygame


class Dame(Piece):
    def __init__(self, color: str):
        """
        une classe pour la pièce [dame]

        Parameters
        ----------
            color : str
                la couleur de la pièce : "n" ou "b"
        """
        super().__init__()

        self.name = "dame"
        self.color = color
        self.value = 8.8

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

        # direction 1:1
        i, j = index
        while i + 1 <= 7 and j + 1 <= 7:
            i += 1
            j += 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction -1:1
        i, j = index
        while i - 1 >= 0 and j + 1 <= 7:
            i -= 1
            j += 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction 1:-1
        i, j = index
        while i + 1 <= 7 and j - 1 >= 0:
            i += 1
            j -= 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction -1:-1
        i, j = index
        while i - 1 >= 0 and j - 1 >= 0:
            i -= 1
            j -= 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction 1:0
        i, j = index
        while i + 1 <= 7:
            i += 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction 0:1
        i, j = index
        while j + 1 <= 7:
            j += 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction 0:-1
        i, j = index
        while j - 1 >= 0:
            j -= 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        # direction -1:0
        i, j = index
        while i - 1 >= 0:
            i -= 1
            if board[i, j] is None:  # case libre
                res.add((i, j))
            elif board[i, j].color != self.color:  # pièce ennemie
                res.add((i, j))
                break
            elif board[i, j].color == self.color:  # pièce alliée
                break

        return res
