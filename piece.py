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

    def move_to(self, board, from_index: tuple({int}), to_index: tuple({int})):
        """
        déplacement de pièce

        Parameters
        ----------
            board : Board
                plateau de jeu
            from_index : tuple
                la position de départ
            to_index : tuple
                la position d'arrivée
        """
        # sauvegarde du mouvement pour coloration des cases
        board.last_move = [from_index, to_index]

        self.number_of_mouv += 1  # la pièce bouge
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
