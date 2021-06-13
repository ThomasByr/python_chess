import pygame
import copy

from player import Player
from board import Board
from human import Human
from new_ai import Ai

from button import Button
from help import Help
from pause import Pause
from play import Play

from clock import Clock

# couleur des pièces
N = "n"
B = "b"

pygame.font.init()
font1 = pygame.font.SysFont("Comic Sans MS", 20)  # police pour l'écriture
font2 = pygame.font.SysFont("Sans-Serif", 15)
font3 = pygame.font.SysFont("Comic Sans MS", 10)
font4 = pygame.font.SysFont("JetBrains Mono Regular", 20)


class Game:
    def __init__(
        self, screen: pygame.Surface, data: dict, settings: dict, display: dict
    ):
        """
        une classe de jeu d'échecs

        Parameters
        ----------
            screen : pygame.Surface
                la surface de jeu
            data : dict
                le dictionnaire des couleurs
            settings : dict
                les réglages de l'ia
            display : dict
                les réglages des graphiques
        """
        self.pause = False  # pour mettre le jeu en pause
        self.new_start = 0.0  # le temps pour redémarer les chronos après la pause
        self.running = True  # le jeu tourne
        self.clock = Clock(-1, 0)  # pour avoir la durée de la partie

        self.screen = screen
        self.data = data
        self.settings = settings
        self.display = display

        self.board = Board()
        self.playerB = Human(B, self)  # joueur avec les pièces blanches
        self.playerN = Ai(N, self)  # joueur avec les pièces noires

        self.cur_player = self.playerB

        self.score = self.board.get_score(self.board.board)
        self.all_scores = [self.score]
        self.all_moves = []  # str
        self.suggested = [(-11, -11), (-11, -11)]

        self.all_buttons = pygame.sprite.Group()
        self.all_buttons.add(Help(self))
        self.all_buttons.add(Pause(self))

    def next_player(self):
        """
        le joueur suivant
        """
        # plus aucun coup n'est suggéré
        self.suggested = [(-11, -11), (-11, -11)]

        # actualisation du score avant l'actualisation de l'état d'échec
        self.score = self.board.get_score(self.board.board)
        # recherche d'une meilleure fonction d'évaluation
        if self.playerB.name in ("aib", "ain") or self.playerN.name in ("aib", "ain"):
            ev = (self.playerB, self.playerN)[self.playerN.name in ("aib", "ain")]
            try:
                ev.engine.set_position(self.all_moves)
                self.score = ev.engine.get_evaluation()["value"] / 256
            except:
                pass

        self.all_scores.append(self.score)

        # actualisation de tous les coups
        self.all_moves.append(self.get_move() + self.board.last_move_addon)
        self.board.last_move_addon = ""

        # actualisation de l'état d'échec
        self.board.get_check(self.playerB, self.playerN)

        self.cur_player = (self.playerB, self.playerN)[self.cur_player == self.playerB]

        self.cur_player.is_mate(self)  # test du mat
        if self.cur_player.checkmate:
            self.running = False  # le joueur ne peut plus jouer

    def get_move(self) -> str:
        move = self.board.last_move
        indexes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        y1 = str(8 - move[0][0])
        y2 = str(8 - move[1][0])
        x1 = indexes[move[0][1]]
        x2 = indexes[move[1][1]]
        return x1 + y1 + x2 + y2

    def display_score(self):
        """
        affichage du graphique du score
        """
        all_scores = self.all_scores
        n = len(all_scores)
        if n == 1:
            all_scores.append(all_scores[0])
            n += 1
        screen = self.screen

        # le coefficient de zoom
        zoom = self.display["zoom_coef"]

        # espacement
        space = 250 // n

        # parcours des scores
        for i in range(n - 1):
            y1 = 300 - all_scores[0] * zoom
            y2 = 300 - all_scores[1] * zoom
            if y1 * y2 < 0:  # on passe par 0
                m = 1 / (y2 - y1)
                b = m * (-i * space)
                # résolution de mx+b=0
                x = -b / m
                self.draw_polygon([(525 + i * space, y1), (525 + x, 300)])
                self.draw_polygon([(525 + x, 300), (525 + (i + 1) * space, y2)])
            else:  # on ne passe pas par 0
                self.draw_polygon([(525 + i * space, y1), (525 + (i + 1) * space, y2)])

    def draw_polygon(self, l: list({tuple({int})})):
        # les points
        x1 = l[0][0]
        y1 = l[0][1]
        x2 = l[1][0]
        y2 = l[1][1]
        l0 = l + [(x2, 300), (x1, 300)]

        # toutes les couleurs
        c1 = self.data["score_graph_if_positiv_color"]
        c2 = self.data["score_graph_if_positiv_color_faded"]
        c3 = self.data["score_graph_if_negativ_color"]
        c4 = self.data["score_graph_if_negativ_color_faded"]

        c = (c1, c3)[y1 <= 0 and y2 <= 0]
        cf = (c2, c4)[y2 <= 0 and y2 <= 0]

        pygame.draw.polygon(self.screen, cf, l0)
        pygame.draw.line(self.screen, c, l[0], l[1])

    def display_state(self):
        """
        affichage de l'état de la partie
        """
        screen = self.screen
        data = self.data
        add = 150

        for i in (1, 2):
            textsurface = font1.render(f"joueur {i}", True, data["player_text_color"])
            screen.blit(textsurface, (510 + add * (i - 1), 1))
            player = (self.playerB, self.playerN)[i == 2]
            name = ("HUMAIN", "I.A.")[player.name in ("aib", "ain")]
            textsurface = font2.render(name, True, data["player_text_color_faded"])
            screen.blit(textsurface, (520 + add * (i - 1), 25))

        if self.cur_player.name in ("humanb", "aib"):  # tour du joueur b
            pygame.draw.lines(
                screen,
                data["active_player_indicator_color"],
                True,
                [(501, 11), (511, 15), (501, 19)],
            )
        if self.cur_player.name in ("humann", "ain"):  # tour du joueur n
            pygame.draw.lines(
                screen,
                data["active_player_indicator_color"],
                True,
                [(651, 11), (661, 15), (651, 19)],
            )

        # afficher le score
        score = round(self.score, 2)
        color = (data["score_if_positiv_color"], data["score_if_negativ_color"])[
            score < 0
        ]
        score += 0.0  # on évite l'affichage de -0.0
        textsurface = font3.render(str(score), True, color)
        screen.blit(textsurface, (570, 20))

        if not self.running:  # afficher l'échec-et-mat
            if self.playerB.checkmate:
                textsurface = font2.render(
                    "checkmate!", True, data["checkmate_indicator_color"]
                )
                screen.blit(textsurface, (520, 35))
            if self.playerN.checkmate:
                textsurface = font2.render(
                    "checkmate!", True, data["checkmate_indicator_color"]
                )
                screen.blit(textsurface, (670, 35))

        else:
            # afficher l'état d'échec des rois
            if self.playerB.check == True:
                textsurface = font2.render("check!", True, data["check_indictor_color"])
                screen.blit(textsurface, (520, 35))
            if self.playerN.check == True:
                textsurface = font2.render("check!", True, data["check_indictor_color"])
                screen.blit(textsurface, (670, 35))

        # afficher la durée de la partie
        h, m, s = self.clock.get_time()
        textsurface = font4.render(
            str(h) + ":" + str(m) + ":" + str(s), True, data["game_duration_color"]
        )
        screen.blit(textsurface, (500, 480))

    def switch_button(self):
        for button in self.all_buttons:
            if button.action == 3:  # bouton pause
                self.all_buttons.remove(button)
                self.all_buttons.add(Play(self))
            if button.action == 4:  # bouton play
                self.all_buttons.remove(button)
                self.all_buttons.add(Pause(self))
