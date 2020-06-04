from piece import Piece
import pygame


class Roi(Piece):
    def __init__(self, color: str, load: bool = True):
        """
        une classe pour la pièce [roi]

        Parameters
        ----------
            color : str
                la couleur de la pièce : "n" ou "b"
        """
        super().__init__()

        self.name = "roi"
        self.color = color
        self.value = 10.0  # !valeur provisoire

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
        # pour le rock, .is_rock_possible est réinitialisé dans Board.deselect_all()
        res = set()

        res.add((index[0] + 1, index[1] + 1))
        res.add((index[0] + 1, index[1] - 1))
        res.add((index[0] + 1, index[1]))

        res.add((index[0] - 1, index[1] + 1))
        res.add((index[0] - 1, index[1] - 1))
        res.add((index[0] - 1, index[1]))

        res.add((index[0], index[1] + 1))
        res.add((index[0], index[1] - 1))

        # rock blanc ou rock noir
        y = (7, 0)[self.color == "n"]

        if self.number_of_mouv == 0 and not self.ever_checked:
            tour1 = board[y, 7]  # petit rock
            tour2 = board[y, 0]  # grand rock

            if tour1 is not None:  # si la tour est bien là
                if tour1.number_of_mouv == 0:  # si la tour n'a pas bougé
                    # si les palces sont libres
                    if board[y, 6] is None and board[y, 5] is None:
                        res.add((y, 6))  # la position est atteignable
                        self.is_rock_possible = True
                        tour1.is_rock_possible = True

            if tour2 is not None:  # si la tour est bien là
                if tour2.number_of_mouv == 0:  # si la tour n'a pas bougé
                    # si les places sont libres
                    if (
                        board[y, 3] is None
                        and board[y, 2] is None
                        and board[y, 1] is None
                    ):
                        res.add((y, 1))
                        self.is_rock_possible = True
                        tour2.is_rock_possible = True

        return res
