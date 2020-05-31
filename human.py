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
            # clique sur une case vide
            if game.board.board[index] is None:
                from_index = game.board.get_selected()
                if from_index is not None:
                    piece = game.board.board[from_index]
                    if piece is not None:  # déplacer la pièce
                        if index in piece.viable:

                            # rock
                            if piece.is_rock_possible and index in (
                                (7, 6),
                                (7, 1),
                                (0, 6),
                                (0, 1),
                            ):
                                if index[1] == 6:
                                    tour = game.board.board[index[0], index[1] + 1]
                                    piece.move_to(game.board, from_index, index)
                                    tour.move_to(
                                        game.board,
                                        (index[0], index[1] + 1),
                                        (index[0], index[1] - 1),
                                    )
                                else:
                                    tour = game.board.board[index[0], index[1] - 1]
                                    piece.move_to(game.board, from_index, index)
                                    tour.move_to(
                                        game.board,
                                        (index[0], index[1] - 1),
                                        (index[0], index[1] + 1),
                                    )

                            # déplacement "standard"
                            else:
                                piece.move_to(game.board, from_index, index)

                            game.next_player()  # joueur suivant
                game.board.deselect_all()

            # case non vide
            else:
                # clic sur une pièce ennemie
                if game.board.board[index].color != self.color:
                    from_index = game.board.get_selected()
                    if from_index is not None:
                        piece = game.board.board[from_index]
                        if piece is not None:  # déplacer la pièce
                            if index in piece.viable:
                                # supprimer la pièce mangée
                                self.eaten.add(game.board.board[index])
                                game.board.all_pieces.remove(game.board.board[index])
                                piece.move_to(game.board, from_index, index)
                                game.next_player()  # joueur suivant

                    game.board.deselect_all()

                # clic sur une pièce alliée
                elif game.board.board[index].color == self.color:
                    game.board.deselect_all()
                    piece = game.board.board[index]
                    piece.click(game, index)
