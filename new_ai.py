import pygame
import numpy as np
import time
from stockfish import Stockfish

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

        # variables propres
        self.engine = Stockfish(
            path="stockfish/stockfish_13_win_x64_bmi2.exe",
            parameters=self.game.settings["parameters"],
        )
        self.steps = self.game.settings["number_of_steps"]
        self.depth = self.game.settings["depth"]

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

    def get_move(self) -> str:
        move = self.game.board.last_move
        indexes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        y1 = str(8 - move[0][0])
        y2 = str(8 - move[1][0])
        x1 = indexes[move[0][1]]
        x2 = indexes[move[1][1]]
        return x1 + y1 + x2 + y2

    def get_pos(self, move: str) -> list({tuple({int})}):
        indexes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x1, y1, x2, y2 = move[:4]
        x1 = indexes.index(x1)
        x2 = indexes.index(x2)
        y1 = 8 - int(y1)
        y2 = 8 - int(y2)
        return [(y1, x1), (y2, x2)]

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
        joue le coup de l'ia        
        """
        # affichage
        textsurface = font.render("modélisation...", True, self.game.data["ai_thinking_indicator_color"])
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()

        # si l'ia ne joue pas le premier coup de la partie
        if self.game.board.last_move[0][0] >= 0:
            moves = self.game.all_moves  # on récupère les coups précédents
            # !print("last moves :", moves)
            self.engine.set_position(moves)

        # meilleur coup
        self.engine.set_depth(self.depth)
        move = self.engine.get_best_move()
        self.engine.set_depth(2)
        # !print("best move :", move)

        # nouvelle position pour le moteur
        self.engine.set_position([move])
        # !print()
        getpos = self.get_pos(move)
        from_index = getpos[0]
        to_index = getpos[1]

        # affichage
        pygame.draw.rect(self.game.screen, self.game.data["background_color"], (720, 25, 100, 20))
        textsurface = font.render("réflexion...", True, self.game.data["ai_thinking_indicator_color"])
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()

        # préparer les coups
        board = self.game.board.board
        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is not None:
                    piece.viable = piece.accessible(board,
                                                    (i, j)).intersection(self.empty(board, piece.color))
                    piece.viable = piece.accessible_with_checked((i, j), piece.viable, board)

        # jouer le coup
        piece = self.game.board.board[from_index]
        if len(move) == 5:
            piece.promoted = move[4]
        if to_index in piece.viable:
            piece.move_to(self.game, self.game.board.board, from_index, to_index)
        else:
            print("error : illegal move played by ai\nsearching new move...\n")
            self.play_alt()

        self.game.next_player()  # joueur suivant

    def play_alt(self):
        """
        permet à l'ordinateur de jouer son tour 
        """
        self.tree = Node(
            self.color,
            None,
            self.game.board.deep_copy(self.game.board.board),
            ((0, 0), (0, 0)),
        )
        steps = self.steps
        start = time.time()  # durée de la réflexion totale

        # on construit l'arbre des coups
        pygame.draw.rect(self.game.screen, self.game.data["background_color"], (720, 25, 100, 20))
        textsurface = font.render("modélisation...", True, self.game.data["ai_thinking_indicator_color"])
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()
        self.build(self.tree, steps, self.color)

        # on cherche le meilleur coup
        pygame.draw.rect(self.game.screen, self.game.data["background_color"], (720, 25, 100, 20))
        textsurface = font.render("réflexion...", True, self.game.data["ai_thinking_indicator_color"])
        self.game.screen.blit(textsurface, (720, 25))
        pygame.display.flip()
        self.tree.get_values(self.game.board.get_score)

        # on modifie le nombre d'étape au besoin
        end = time.time()
        if end - start <= 0.5 and not self.check:
            if self.steps + 1 <= self.settings["max_number_of_steps"]:
                self.steps += self.settings["number_of_steps_increase_allowed"]

        move = ()
        # on joue ce coup
        for child in self.tree.list_of_leaves:
            if child.value == self.tree.value:
                move = child.move
                break
        from_index = move[0]
        to_index = move[1]
        self.game.board.board[from_index].move_to(self.game, self.game.board.board, from_index, to_index)

        # on passe au joueur suivant
        self.game.next_player()

    def build(self, current_node: Node, remaining_steps: int, color: str):
        if remaining_steps == 0:
            current_node.value = self.game.board.get_score(current_node.board)
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
            piece.viable = piece.accessible(board, from_index).intersection(self.empty(board, piece.color))
            piece.viable = piece.accessible_with_checked(from_index, piece.viable, board)
            # pour chaque déplacement viable
            for to_index in piece.viable:
                new_board = board.copy()

                new_board = self.en_avant_pawn(new_board)
                piece.move_to(None, new_board, from_index, to_index)
                if piece.name == "pion":
                    if to_index[0] == 0 or to_index[0] == 7:
                        new_board[to_index] = Dame(piece.color)

                new_node = Node(
                    color,
                    current_node,
                    new_board,
                    (from_index, to_index),
                )
                color = ("b", "n")[color == "b"]
                current_node.__append__(new_node)
                self.build(new_node, remaining_steps - 1, color)
