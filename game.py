import pygame
import copy

from player import Player
from board import Board
from human import Human
from ai import Ai

from button import Button
from undo import Undo
from redo import Redo
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
    def __init__(self, screen: pygame.Surface, data: dict):
        """
        une classe de jeu d'échecs

        Parameters
        ----------
            screen : pygame.Surface
                la surface de jeu
            data : dict
                le dictionnaire des couleurs
        """

        self.pause = False  # pour mettre le jeu en pause
        self.new_start = 0.0  # le temps pour redémarer les chronos après la pause
        self.running = True  # le jeu tourne
        self.clock = Clock(-1, 0)  # pour avoir la durée de la partie

        self.board = Board()
        # pour la notion de "undo"/"redo"
        self.all_games = [self]

        self.playerB = Human(B)  # joueur avec les pièces blanches
        self.playerN = Human(N)  # joueur avec les pièces noires

        self.cur_player = self.playerB

        self.screen = screen
        self.data = data

        self.score = self.board.get_score(self)

        # état qui permet de dire si on change de tableau avec "undo"/"redo"
        self.changing_board = 0
        self.all_buttons = pygame.sprite.Group()
        # ?le click ne marche pas si l'ordre est changé
        self.all_buttons.add(Redo(self))
        self.all_buttons.add(Undo(self))
        self.all_buttons.add(Pause(self))

    def next_player(self):
        """
        le joueur suivant
        """
        # copie du jeu et de ses pièces avec leurs valeurs propres (notion "undo"/"redo")
        self.all_games.append(copy.copy(self))
        self.changing_board = 0  # on remet le compteur à zéro

        # actualisation du score avant l'actualisation de l'état d'échec
        self.score = self.board.get_score(self)

        # actualisation de l'état d'échec
        self.board.get_check(self.playerB, self.playerN)

        self.cur_player = (self.playerB, self.playerN)[self.cur_player == self.playerB]

        self.cur_player.is_mate(self)  # test du mat
        if self.cur_player.checkmate:
            self.running = False  # le joueur ne peut plus jouer

    def display_state(self):
        """
        affichage de l'état de la partie
        """
        screen = self.screen
        data = self.data
        add = 150

        for i in (1, 2):
            textsurface = font1.render(f"joueur {i}", False, data["player_text_color"])
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
