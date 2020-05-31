import pygame


pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 10)  # police pour l'écriture


class Player:
    def __init__(self):
        """
        une classe générique
        """
        self.name = ""  # initialisation propre dans "human.py" et "ai.py"
        self.color = ""
        self.eaten = pygame.sprite.Group()
        self.check = False  # si le joueur est mis en échec
        self.checkmate = False  # si le joueur est échec-et-mat

    def __eq__(self, other):  # override pour le test d'égalité entre joueurs
        return self.name == other.name

    def pick_and_place(self, name: str, x: int, y: int, z: int):
        """
        permet de placer les pièces mangées

        Parameters
        ----------
            name : str
                le nom de la pièce à placer
            x : int
                sa position en x
            y : int
                sa position en y
            z : int
                sa taille (carré)
        """
        for piece in self.eaten:
            if piece.name == name:
                piece.image = pygame.transform.scale(piece.image, (z, z))
                piece.rect.x = x
                piece.rect.y = y

    def display_eaten(self, screen: pygame.Surface, data: dict):
        """
        affiche les pièces mangées par le joueur

        Parameters
        ----------
            screen : pygame.Surface
                l'écran
            data : dict
                le dictionnaire des couleurs
        """
        temp = {"pion": 0, "cavalier": 0, "fou": 0, "tour": 0, "dame": 0}
        for piece in self.eaten:  # le nombre de chaque pièce que le joueur à mangé
            temp[f"{piece.name}"] += 1

        x = 510 + 150 * (self.color == "n")
        # le nombre de pièces déjà affichées (pour le décalage d'ordonnée)
        nb = 0
        for e in temp:
            if temp[e] == 0:  # si le joueur n'a pas mangé la pièce "e"
                continue
            self.pick_and_place(e, x, 50 + nb, 12)
            textsurface = myfont.render(str(temp[e]), True, data["count_text_color"])
            screen.blit(textsurface, (x + 20, 50 + nb))
            nb += 10
        self.eaten.draw(screen)

    def is_mate(self, game) -> None:
        """
        si le joueur est en échec-et-mat\\
        compte le nombre de mouvement possible par le joueur
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        board = game.board.board
        possible = set()
        # compte le nombre de cases viables pour toutes les pièces du joueur
        for i in range(8):
            for j in range(8):
                piece = board[i, j]
                if piece is not None and piece.color == self.color:
                    viable = piece.accessible(board, (i, j)).intersection(
                        game.board.empty(piece.color)
                    )
                    viable = piece.accessible_with_checked((i, j), viable, game)
                    possible = possible.union(viable)
        # si le joueur ne peut pas déplacer de pièce, alors il est en échec-et-mat
        self.checkmate = possible.__len__() == 0
