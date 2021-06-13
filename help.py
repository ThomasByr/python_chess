import pygame

from button import Button


class Help(Button):
    def __init__(self, game):
        """
        une classe pour le bouton "help"
        
        Parameters
        ----------
            game : Game
                le jeu
        """
        super().__init__()
        self.action = 1
        self.game = game

        self.get_image(self.action)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect.x = 775
        self.rect.y = 475

    def get_pos(self, move: str) -> list({tuple({int})}):
        indexes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x1, y1, x2, y2 = move
        x1 = indexes.index(x1)
        x2 = indexes.index(x2)
        y1 = 8 - int(y1)
        y2 = 8 - int(y2)
        return [(y1, x1), (y2, x2)]

    def click(self):
        game = self.game

        # recherche d'une meilleure fonction d'évaluation
        if game.playerB.name in ("aib", "ain") or game.playerN.name in ("aib", "ain",):
            ev = (game.playerB, game.playerN)[game.playerN.name in ("aib", "ain")]
            try:
                ev.engine.set_position(game.all_moves)
                move = ev.engine.get_best_move()
                game.suggested = self.get_pos(move)
            except:
                print("fonctionnalité désactivée")
