import pygame
import numpy as np


class Piece(pygame.sprite.Sprite):
    def __init__(self):
        """
        une classe générique
        
        NOTE
        ------
        - déplacement spécial : le rock n'est accessible que depuis le clic sur le roi
        - "en passant" et "rock" peuvent déboucher sur des erreurs
        """
        super().__init__()
        self.selected = False  # si la pièce est sélectionnée
        self.viable = set()  # le set de destinations possibles
        # pour le roi (peut-être la dame) : si la pièce à déjà été mise en échec
        self.ever_checked = False  # autorise le rock ou non
        self.check = False  # état courant
        # la valeur de chaque pièce (prendra en compte le positionnement et l'avancement de la partie)
        self.value = 0.0
        # le nombre de mouvements de la pièce (utile pour le rock)
        self.number_of_mouv = 0
        # pour le roi et la tour : si le rock est possible
        self.is_rock_possible = False
        # pour les pions :
        self.pawn_forward = 0  # le nombre de tours suivant la sortie de deux cases
        self.promoted = None  # Q, R, B, N (dame, tour, fou, cavalier)

    def get_image(self, piece, color):
        """
        donne l'image à une piece

        Parameters
        ----------
            piece : str
                le nom de la piece : "pion", "tour", "cavalier", "fou", "roi", "dame"
            color : str
                la couleur de la pièce : "n" ou "b"
        """
        self.image = pygame.image.load(f"images/{piece}_{color}.png")
        self.rect = self.image.get_rect()

    def click(self, game, index: tuple({int})):
        """
        fonction lorsque l'on clique sur une pièce de sa couleur

        Parameters
        ----------
            game : Game
                le jeu
            index : tuple
                la position de la pièce
        """
        self.selected = True
        self.viable = self.accessible(game.board.board, index).intersection(
            game.board.empty(self.color))

        self.viable = self.accessible_with_checked(index, self.viable,
                                                   game.board.board)

    def move_to(self, game, board: np.array, from_index: tuple({int}),
                to_index: tuple({int})):
        """
        déplacement de pièce

        Parameters
        ----------
            game : Game
                le jeu
            board : np.array
            from_index : tuple
                la position de départ
            to_index : tuple
                la position d'arrivée
        """

        # à chaque déplacement de pièce, Piece.pawn_forward change
        if game is not None:
            game.board.en_avant_pawn()

        # rock
        if self.is_rock_possible and to_index in ((7, 6), (7, 2), (0, 6),
                                                  (0, 2)):
            if to_index[1] == 6 and board[to_index[0],
                                          7] is not None:  # petit rock
                tour = board[to_index[0], 7]
                tour.move_to(
                    game,
                    board,
                    (to_index[0], 7),
                    (to_index[0], 5),
                )
            elif to_index[1] == 2 and board[to_index[0],
                                            0] is not None:  # grand rock
                tour = board[to_index[0], 0]
                tour.move_to(
                    game,
                    board,
                    (to_index[0], 0),
                    (to_index[0], 3),
                )

        # initialisation de "en passant"
        if self.name == "pion":
            # test de déplacement de deux vers l'avant
            if to_index[0] - 2 == from_index[
                    0] or to_index[0] + 2 == from_index[0]:
                self.pawn_forward = 1

        # utilisation de "en passant"
        if self.name == "pion":
            # si le pion se déplace en diagonale mais qu'il n'y a aucune pièce sur la case d'arrivée
            if to_index[0] - from_index[0] != 0 and to_index[1] - from_index[
                    1] != 0:
                if board[to_index] == None:
                    if self.color == "b":  # en passant blanc
                        other = board[to_index[0] + 1, to_index[1]]
                        # le joueur mange la pièce et on enlève la pièce aux pièces à dessiner
                        if game is not None:
                            game.cur_player.eaten.add(other)
                            game.board.all_pieces.remove(other)
                        # comme le pion n'arrive pas sur une pièce ennemie, on enlève la pièce
                        board[to_index[0] + 1, to_index[1]] = None
                    if self.color == "n":  # en passant noir
                        other = board[to_index[0] - 1, to_index[1]]
                        # le joueur mange la pièce et on enlève la pièce aux pièces à dessiner
                        if game is not None:
                            game.cur_player.eaten.add(other)
                            game.board.all_pieces.remove(other)
                        # comme le pion n'arrive pas sur une pièce ennemie, on enlève la pièce
                        board[to_index[0] - 1, to_index[1]] = None

        # si la pièce arrive sur une pièce ennemie
        other = board[to_index]
        if game is not None and other is not None and other.color != self.color:
            # le joueur mange la pièce et on enlève la pièce aux pièces à dessiner
            game.cur_player.eaten.add(other)
            game.board.all_pieces.remove(other)

        if game is not None:
            # sauvegarde du mouvement pour coloration des cases
            game.board.last_move = [from_index, to_index]

        # déplacer la pièce
        self.number_of_mouv += 1
        piece = board[from_index]
        board[from_index] = None
        board[to_index] = piece

        # changement du pion en dame
        if game is not None and self.name == "pion":
            if to_index[0] == 0 or to_index[0] == 7:
                # on enlève le pion des pièces à dessiner et on le change en dame
                game.board.all_pieces.remove(self)
                game.board.change_pawn(to_index, self.promoted, self.color)
                game.board.last_move_addon = (
                    "q", self.promoted)[self.promoted is not None]

    def accessible_with_checked(self, from_index: tuple({int}),
                                set_of_index: set({tuple({int})}),
                                raw_board) -> tuple({int}):
        """
        donne l'ensemble des cases disponibles\\
        qui terminent l'état d'échec ou qui l'évitent
        
        Parameters
        ----------
            from_index : tuple
                la position de la pièce
            set_of_index : set
                ensemble des déplacements viables
                indépendament de l'état d'échec
            raw_board : np.Array
                le plateau
        Returns
        -------
            tuple : ensemble des cases
        """
        base_board = raw_board.copy()
        board = base_board.copy()
        color = self.color
        res = set()

        def empty(c: str) -> set({tuple({int})}):
            empty_set = set()
            for i in range(8):  # parcours du plateau
                for j in range(8):
                    piece = board[i, j]
                    if piece is None or piece.color != c:
                        empty_set.add((i, j))
            return empty_set

        def get_check():
            check = False
            for i in range(8):  # parcours du plateau
                for j in range(8):
                    piece = board[i, j]
                    if piece is not None and piece.color != color:
                        viable = piece.accessible(board, (i, j)).intersection(
                            empty(piece.color))
                        for viable_index in viable:
                            other = board[viable_index]
                            if other is not None and other.name == "roi":
                                check = True
            return check

        for index in set_of_index:
            piece = board[from_index]
            board[from_index] = None
            board[index] = piece
            if not get_check():
                res.add(index)
            board = base_board.copy()

        return res
