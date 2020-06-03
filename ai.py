import pygame
import numpy as np

from player import Player

from node import Node
from piece import Piece
from pion import Pion
from dame import Dame

pygame.font.init()
font = pygame.font.SysFont("JetBrains Mono Regular", 15)


class Ai(Player):
    def __init__(self, color: str, game):
        """
        une classe pour l'ordinateur

        Parameters
        ----------
            color : str
                la couleur des pièces
            game: Game
                le jeu
        """
        super().__init__()
        self.name = f"ai{color}"
        self.color = color
        self.check = False
        self.game = game

        # l'arbre des tableaux (valeur propre au joueur Ai)
        self.tree = Node(
            self.color, None, self.game.board.board.copy(), ((0, 0), (0, 0))
        )

    def en_avant_pawn(self, board) -> np.array:
        """
        clone de la méthode de la classe Board\\
        ne modifie pas les valeurs étant donné qu'on ne déplace pas de pièces dans le tableau courant\\
        mais dans des tableaux provisoires
        """
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = board[i, j]
                if piece is not None:
                    if piece.pawn_forward >= 2:
                        piece.pawn_forward = 0
                    piece.pawn_forward += piece.pawn_forward
        return board

    def empty(self, board, color: str) -> set({tuple({int})}):
        """
        clone de la méthode de la classe Board\\
        ne modifie pas les valeurs étant donné qu'on ne déplace pas de pièces dans le tableau courant\\
        mais dans des tableaux provisoires
        """
        res = set()
        for i in range(8):  # ligne
            for j in range(8):  # colonne
                piece = board[i, j]
                if piece is None or piece.color != color:
                    res.add((i, j))
        return res

    def play(self):
        """
        permet à l'ordinateur de jouer son tour 
        """
        self.tree = Node(
            self.color, None, self.game.board.board.copy(), ((0, 0), (0, 0))
        )
        settings = self.game.settings
        steps = settings["number_of_steps"]

        # on construit l'arbre des coups
        textsurface = font.render(
            "modélisation...", True, self.game.data["ai_thinking_indicator_color"]
        )
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()
        self.build(self.tree, steps, self.color)

        # on cherche le meilleur coup
        pygame.draw.rect(
            self.game.screen, self.game.data["background_color"], (720, 25, 100, 20)
        )
        textsurface = font.render(
            "réflexion...", True, self.game.data["ai_thinking_indicator_color"]
        )
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()
        self.tree.get_values(self.game.board.get_score)

        move = ()
        # on joue ce coup
        for child in self.tree.list_of_leaves:
            if child.value == self.tree.value:
                move = child.move
        from_index = move[0]
        to_index = move[1]
        self.game.board.board[from_index].move_to(
            self.game, self.game.board.board, from_index, to_index
        )

        # on passe au joueur suivant
        self.game.next_player()

    def build(self, current_node: Node, remaining_steps: int, color: str):
        if remaining_steps == 0:
            return

        board = current_node.board.copy()
        list_of_pieces = []
        # création de la liste des pièces de la bonne couleur
        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is not None and piece.color == color:
                    list_of_pieces.append((piece, (i, j)))

        # pour chaque pièce
        for piece, from_index in list_of_pieces:
            piece.viable = piece.accessible(board, from_index).intersection(
                self.empty(board, piece.color)
            )
            piece.viable = piece.accessible_with_checked(
                from_index, piece.viable, board
            )
            # pour chaque déplacement viable
            for to_index in piece.viable:
                new_board = board.copy()

                new_board = self.en_avant_pawn(new_board)
                piece.move_to(None, new_board, from_index, to_index)
                if piece.name == "pion":
                    if to_index[0] == 0 or to_index[0] == 7:
                        new_board[to_index] = Dame(piece.color)

                new_node = Node(
                    color, current_node, new_board.copy(), (from_index, to_index)
                )
                color = ("b", "n")[color == "b"]
                current_node.__append__(new_node)
                self.build(new_node, remaining_steps - 1, color)
