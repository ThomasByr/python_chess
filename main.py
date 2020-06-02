import json
import pygame
import numpy as np

from game import Game


"""
Chess.py
========
> Merci de lire REDAME.md avant de commencer l'utilisation
version
-------
    version courrante : 0.a10
    première sortie : 25 mai 2020 (v.0.a01)
    dernière mise à jour : 1er juin 2020
auteurs
-------
    auteur principal : Thomas B
    chef de projet : Thomas B
    tests et débuggage : "xxxxxxxxxxxxxx"
contacts
--------
    github : https://github.com/Thomas2-bot
    mail (disponible via github) : thomas-c2000@outlook.fr
"""


# %% paramètres
with open("settings/colors.json", "r") as settings:
    data = json.load(settings)


# %% initialisation de pygame
pygame.init()
time = pygame.time.Clock()


# %% générer la fenêtre
pygame.display.set_caption("Chess.py")
screen = pygame.display.set_mode((800, 500))

# arrière plan
screen.fill(data["background_color"])
background = pygame.image.load("images/chess_board.jpg")
background = pygame.transform.scale(background, (500, 500))


# %% boucle principale
running = True
game = Game(screen, data)
pos = (-1000, -1000)  # position initiale du curseur en dehors de l'écran

# vérification des joueurs (joueurs modifiables dans "game.py")
assert (
    not game.playerB.color == game.playerN.color
), "merci de choisir des couleurs de joueurs différentes"


while running:
    screen.fill(data["background_color"])  # couleur de fond
    screen.blit(background, (0, 0))  # dessin du plateau

    # lance le tour de l'ia si aucun des joueur n'a mat
    if game.running and game.cur_player.name in ("aib", "ain"):
        game.cur_player.play(game)

    for event in pygame.event.get():
        # si le joueur ferme cette fenêtre
        if event.type == pygame.QUIT:
            running = False

        # si le joueur clique sur une case
        if event.type == pygame.MOUSEBUTTONUP:
            # position de la souris
            pos = pygame.mouse.get_pos()  # tuple (x, y) : 0, 0 en haut à gauche
            index = 8 * pos[1] // 500, 8 * pos[0] // 500  # coordonnées de la case

            # si aucun des joueurs n'a mat et que le joueur est humain
            if game.running and game.cur_player.name in ("humanb", "humann"):
                game.cur_player.click_tests(game, index)
                game.board.selected = game.board.get_selected()

            clicked_button = [
                sprite for sprite in game.all_buttons if sprite.rect.collidepoint(pos)
            ]
            if len(clicked_button):
                clicked_button[0].click()
                if clicked_button[0].action == 3:
                    game.switch_button()

    # mettre à jour l'affichage
    game.display_state()  # état du jeu
    game.playerB.display_eaten(screen, data)  # pièces mangées
    game.playerN.display_eaten(screen, data)
    game.board.draw_last_move(screen, data)  # dessin du dernier déplacement
    game.board.update(screen)  # dessin des pièces
    if game.board.selected is not None:  # cases de déplacement viables
        game.board.draw_viable(
            screen, game.board.board[game.board.selected].viable, data
        )
    game.board.draw_square(screen, pos, data)  # case sélectionnée
    game.all_buttons.draw(screen)  # dessinner les boutons

    pygame.display.flip()

    while game.pause:  # mise en pause du jeu
        for event in pygame.event.get():
            # si le joueur ferme la fenêtre
            if event.type == pygame.QUIT:
                game.pause = False
                running = False

            # si le joueur clique sur un bouton "pause"/"play"
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_button = [  # normalement seul le bouton 4 est disponible
                    sprite
                    for sprite in game.all_buttons
                    if sprite.rect.collidepoint(pos) and sprite.action in (3, 4)
                ]
                if len(clicked_button):
                    clicked_button[0].click()
                    game.switch_button()

        game.all_buttons.draw(screen)  # dessinner les boutons
        pygame.display.flip()
        time.tick(1)  # éconnomie d'énergie

    time.tick(60)  # ?60 ips


pygame.quit()  # !fermer le jeu proprement
