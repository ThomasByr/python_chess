import numpy as np
import pygame
import copy

from piece import Piece
from pion import Pion
from fou import Fou
from tour import Tour
from cavalier import Cavalier
from roi import Roi
from dame import Dame


# couleur des pièces
N = "n"
B = "b"


class Board:
    def __init__(self):
        """
        une classe de plateau pour échiquier
        """

        # initialiser les positions
        self.board = np.array(
            [
                [
                    Tour(N),
                    Cavalier(N),
                    Fou(N),
                    Dame(N),
                    Roi(N),
                    Fou(N),
                    Cavalier(N),
                    Tour(N),
                ],
                [
                    Pion(N),
                    Pion(N),
                    Pion(N),
                    Pion(N),
                    Pion(N),
                    Pion(N),
                    Pion(N),
                    Pion(N),
                ],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [
                    Pion(B),
                    Pion(B),
                    Pion(B),
                    Pion(B),
                    Pion(B),
                    Pion(B),
                    Pion(B),
                    Pion(B),
                ],
                [
                    Tour(B),
                    Cavalier(B),
                    Fou(B),
                    Dame(B),
                    Roi(B),
                    Fou(B),
                    Cavalier(B),
                    Tour(B),
                ],
            ],
        )
        self.all_pieces = pygame.sprite.Group()
        self.selected = None
        self.last_move = [(-10, -10), (-11, -11)]

        # positions intrinsèques initialies des pièces
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is not None:
                    piece.rect.y = i * 500 // 8 + 2
                    piece.rect.x = j * 500 // 8 + 2
                    self.all_pieces.add(piece)

    @staticmethod
    def deep_copy(board: np.array) -> np.array:
        new_board = np.array([[None for _ in range(8)] for _ in range(8)])
        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is not None:
                    if piece.name == "pion":
                        new_board[i, j] = Pion(piece.color)
                    if piece.name == "cavalier":
                        new_board[i, j] = Cavalier(piece.color)
                    if piece.name == "fou":
                        new_board[i, j] = Fou(piece.color)
                    if piece.name == "tour":
                        new_board[i, j] = Tour(piece.color)
                    if piece.name == "dame":
                        new_board[i, j] = Dame(piece.color)
                    if piece.name == "roi":
                        new_board[i, j] = Roi(piece.color)
                    new_board[i, j].ever_checked = copy.deepcopy(piece.ever_checked)
                    new_board[i, j].check = copy.deepcopy(piece.check)
                    new_board[i, j].number_of_mouv = copy.deepcopy(piece.number_of_mouv)
                    new_board[i, j].is_rock_possible = copy.deepcopy(
                        piece.is_rock_possible
                    )
                    new_board[i, j].pawn_forward = copy.deepcopy(piece.pawn_forward)
        return new_board

    def empty(self, color: str) -> set({tuple({int})}):
        """
        donne les cases vides

        Parameters
        ----------
            color : str
                la couleur de la pièce en jeu
        Returns
        -------
            set : le set des cases viables pour une couleur
        """
        res = set()
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is None or piece.color != color:
                    res.add((i, j))
        return res

    def update(self, screen: pygame.Surface):
        """
        actualise l'affichage de l'écran

        Parameters
        ----------
            screen : pygame.Surface
                la surface sur laquelle on dessine
        """
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is not None:
                    piece.rect.y = i * 500 // 8 + 2
                    piece.rect.x = j * 500 // 8 + 2
        self.all_pieces.draw(screen)

    def deselect_all(self) -> None:
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is not None:
                    piece.selected = False  # on déselectionne la pièce
                    piece.is_rock_possible = False  # le rock n'est plus demandé

    def en_avant_pawn(self) -> None:
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is not None:
                    if piece.pawn_forward >= 2:
                        piece.pawn_forward = 0
                    piece.pawn_forward += piece.pawn_forward

    def get_selected(self):
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = self.board[i, j]
                if piece is not None and piece.selected == True:
                    return (i, j)
        return None

    def draw_square(self, screen: pygame.Surface, pos: tuple({int}), data: dict):
        """
        dessine un carré sur la case sélectionnée

        Parameters
        ----------
            screen : pygame.Surface
                la surface de dessin
            pos : tuple
                la position du curseur
                (x, y) : 0, 0 en haut à gauche
            data : dict
                le dictionnaire des couleurs
        """
        if 0 <= pos[0] <= 500:
            x = int((pos[0] / 500) * 8) * 500 // 8
            y = int((pos[1] / 500) * 8) * 500 // 8
            pygame.draw.rect(
                screen, data["selected_rect_color"], (x, y, 500 // 8, 500 // 8), 3
            )

    def draw_viable(
        self, screen: pygame.Surface, viable: set({tuple({int})}), data: dict
    ):
        """
        dessine un rond sur chaque case de déplacement viable

        Parameters
        ----------
            screen : pygame.Surface
                la surface de dessin
            viable : set
                le set de positions viables de la pièce sélectionnée
            data : dict
                le dictionnaire des couleurs
        """
        for pos in viable:
            x = pos[1] * (500 // 8) + 34
            y = pos[0] * (500 // 8) + 34
            pygame.draw.circle(screen, data["viable_case_color"], (x, y), 5)

    def draw_last_move(self, screen: pygame.Surface, data: dict):
        """
        dessine un carré vert sur le dernier mouvement\\
        mis à jour lors de l'appel Piece.move_to()
        
        Parameters
        ----------
            screen : pygame.Surface
                la surface de dessin
            data : dict
                le dictionnaire des couleurs
        """
        from_index = self.last_move[0]
        to_index = self.last_move[1]
        x1 = from_index[1] * 500 // 8
        y1 = from_index[0] * 500 // 8
        x2 = to_index[1] * 500 // 8
        y2 = to_index[0] * 500 // 8
        choices = (
            data["last_move_overlay_light_color"],
            data["last_move_overlay_dark_color"],
        )
        if 0 <= x1 <= 500 and 0 <= y1 <= 500 and 0 <= x2 <= 500 and 0 <= y2 <= 500:
            # couleur claire pour les cases blanches et foncée pour les cases bleues
            c1 = choices[(from_index[0] + from_index[1]) % 2]
            c2 = choices[(to_index[0] + to_index[1]) % 2]
            # ajustement de 1px pour les cases bleues
            x1 += (from_index[0] + from_index[1]) % 2
            y1 += (from_index[0] + from_index[1]) % 2
            x2 += (to_index[0] + to_index[1]) % 2
            y2 += (to_index[0] + to_index[1]) % 2
            pygame.draw.rect(screen, c1, (x1, y1, 500 // 8, 500 // 8))
            pygame.draw.rect(screen, c2, (x2, y2, 500 // 8, 500 // 8))

    @staticmethod
    def get_score(board: np.array) -> float:
        """
        donne le score basé sur les pièces blanches\\
        on donne aussi l'état d'échec à toute les pièces au besoin\\
        méthode de calcul provisoire
        
        Parameters
        ----------
            board : np.array
                le plateau
        Returns
        ---------
            float : le score du plateau
        """
        score = 0.0

        def empty(color: str) -> set({tuple({int})}):
            res = set()
            for i in range(8):  # ligne
                for j in range(8):  # colonne
                    piece = board[i, j]
                    if piece is None or piece.color != color:
                        res.add((i, j))
            return res

        # réinitialisation de la mise en échec des pièces
        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is not None:
                    piece.check = False

        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is None:
                    continue

                temp = piece.value  # score temporel

                if i in (0, 7) or j in (0, 7):  # si la pièce est sur le bord
                    temp /= 1.10

                viable = piece.accessible(board, (i, j)).intersection(
                    empty(piece.color)
                )
                for index in viable:
                    other = board[index]
                    if other is not None and other.color != piece.color:
                        # on met l'état "échec" sur la pièce ennemie
                        other.ever_checked = True  # à ne pas réinitialiser
                        other.check = True  # réinitialisation à chaque appel
                        # si la pièce menace une ou plusieurs pièces plus "importantes"
                        temp += (
                            (other.value - piece.value)
                            * (piece.value < other.value)
                            / other.value
                        )
                        # score à ajouter si échec du joueur adverse (le roi vaut 0 : valeur provisoire)
                        if other.name == "roi":
                            temp += 3 / piece.value

                score += temp * (1, -1)[piece.color == "n"]

        return score

    def get_check(self, playerB, playerN) -> None:
        """
        modifie les valeur des joueurs\\
        donne l'état d'échec des deux joueur
        
        Parameters
        ----------
            playerB : Player
                le joueur des pièces blanches
            playerN : Player
                le joueur des pièces noires
        """
        playerB.check = False  # réinitialisation de l'état
        playerN.check = False
        for i in range(8):  # parcours du plateau
            for j in range(8):
                piece = self.board[i, j]
                if piece is not None and piece.name == "roi":  # recherche du roi
                    if piece.check == True and piece.color == "b":
                        playerB.check = True
                    elif piece.check == True and piece.color == "n":
                        playerN.check = True

    def change_pawn(self, index: tuple({int}), color: str) -> None:
        """
        change le pion en dame lorsqu'il arrive en fin de plateau
        
        Parameters
        ----------
            index : tuple
                la position du pion sur le plateau
            color : str
                la couleur du pion
        """
        # on place la dame sur le plateau et on l'ajoute aux pièces à dessiner
        self.board[index] = Dame(color)
        self.all_pieces.add(self.board[index])
