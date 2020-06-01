import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self):
        """
        une classe générique
        
        NOTE
        ------
        - déplacement spécial : le rock n'est accessible que depuis le clic sur le roi
        - "en passant" n'est pas encore implémenté
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
        # pour les pions : le nombre de tours suivant la sortie de deux cases du pions
        self.pawn_forward = 0

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
            game.board.empty(self.color)
        )

        self.viable = self.accessible_with_checked(index, self.viable, game)

    def move_to(self, game, from_index: tuple({int}), to_index: tuple({int})):
        """
        déplacement de pièce

        Parameters
        ----------
            game : Game
                le jeu
            from_index : tuple
                la position de départ
            to_index : tuple
                la position d'arrivée
        """
        board = game.board

        # à chaque déplacement de pièce, Piece.pawn_forward change
        board.en_avant_pawn()

        # rock
        if self.is_rock_possible and to_index in ((7, 6), (7, 1), (0, 6), (0, 1)):
            if to_index[1] == 6:  # petit rock
                tour = board.board[to_index[0], to_index[1] + 1]
                tour.move_to(
                    game,
                    (to_index[0], to_index[1] + 1),
                    (to_index[0], to_index[1] - 1),
                )
            else:  # grand rock
                tour = board.board[to_index[0], to_index[1] - 1]
                tour.move_to(
                    game,
                    (to_index[0], to_index[1] - 1),
                    (to_index[0], to_index[1] + 1),
                )

        # initialisation de "en passant"
        if self.name == "pion":
            # test de déplacement de deux vers l'avant
            if to_index[0] - 2 == from_index[0] or to_index[0] + 2 == from_index[0]:
                self.pawn_forward = 1

        # utilisation de "en passant"
        if self.name == "pion":
            # si le pion se déplace en diagonale mais qu'il n'y a aucune pièce sur la case d'arrivée
            if to_index[0] - from_index[0] != 0 and to_index[1] - from_index[1] != 0:
                if board.board[to_index] == None:
                    if self.color == "b":  # en passant blanc
                        other = board.board[to_index[0] + 1, to_index[1]]
                        game.cur_player.eaten.add(other)
                        board.all_pieces.remove(other)
                    if self.color == "n":  # en passant noir
                        other = board.board[to_index[0] - 1, to_index[1]]
                        game.cur_player.eaten.add(other)
                        board.all_pieces.remove(other)

        # si la pièce arrive sur une pièce ennemie
        other = board.board[to_index]
        if other is not None and other.color != self.color:
            game.cur_player.eaten.add(other)
            board.all_pieces.remove(other)

        # sauvegarde du mouvement pour coloration des cases
        board.last_move = [from_index, to_index]

        # déplacer la pièce
        self.number_of_mouv += 1
        piece = board.board[from_index]
        board.board[from_index] = None
        board.board[to_index] = piece

    def accessible_with_checked(
        self, from_index: tuple({int}), set_of_index: set({tuple({int})}), game
    ) -> tuple({int}):
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
            game : Game
                le jeu
        Returns
        -------
            tuple : ensemble des cases
        """
        base_board = game.board.board.copy()
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
                            empty(piece.color)
                        )
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
