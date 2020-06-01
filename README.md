# Documentation de `Chess.py`<sub>(v.0.a09)</sub>

1. [Implémentation et explications](#implémentation-et-explications)
   1. [Classe `Game`](#classe-game)
   2. [Classe `Player` et sous-classes](#classe-player-et-sous-classes)
   3. [Classe `Piece` et sous-classes](#classe-piece-et-sous-classes)
   4. [Classe `Board`](#classe-board)
   5. [Classe `Button` et sous-classes](#classe-button-et-sous-classes)
   6. [Classe ``Clock``](#classe-clock)
2. [Librairies et autre prérequis](#librairies-et-autre-prérequis)
3. [Mises à jour](#mises-à-jour)
4. [Changelog](#changelog)

> exécution du programme grâce à `main.py`

Cet ensemble d'algorithmes a pour but d'implémenter en Python le célèbre jeu des échecs, dont les règles furent fixées au XV<sup>e</sup> siècle. Il est possible de jouer contre une autre personne ou contre l'algorithme intégré. Il est maintenant possible (à partir de la version 0.a05) de laisser jouer l'ordinateur contre lui-même.

L'interface grapique à été faite grâce à [Pygame](https://www.pygame.org/). Le programme tourne actuellement sous python 3.8.3, mais des compatibilités sont possibles pour python 3.6.4 et au-delà.

## Implémentation et explications

Un programmeur amateur aura remarqué l'orientation objet de ce programme. En effet, même si il est possible de tout faire sans, il est plus aisé de se retrouver dans le code lorsque celui-ci est organisé en classes séparées dans différents fichiers.

> il est recommendé de lire les commentaires et les docstrings qui sont présents dans tous les fichiers

### Classe ``Game``

C'est la classe "principale" de ce programme. C'est elle qui comporte les liens vers toutes les autres classes. Elle permet de gérer entre autres les deux joueurs ainsi que le plateau de jeu. Elle est fortement dépendante de pygame et se trouve dans le fichier [game.py](game.py).

### Classe ``Player`` et sous-classes

C'est la classe qui gère les actions que le joueur à cerveau organique ou de cilicone peut faire tout au long de la partie. Ses sous-classes sont les classes Humain et Ai. Ces fichiers sont disponibles dans [player.py](player.py), [human.py](human.py) et [ai.py](ai.py). Le joueur humain peut ainsi déplacer des pièces en cliquant sur les pièces et ensuite sur les cases indiquées comme étant des déplacements viables (voir la [sous section suivante](#classe-piece-et-sous-classes) pour plus de détails sur les déplacements). Dans les versions _beta_ et ultérieures la partie ia devrait jouer au lieu de passer son tour.

### Classe ``Piece`` et sous-classes

C'est la classe qui implémente la notion de pièces ainsi que leurs mouvements. Les rocks ont été implémentés (à partir de la v.0.a02) et lors d'un échec, les cases disponibles sont réduites en conséquence (à partir de la v.0.a03). Les pions ne peuvent malheureusement pas encore prendre un pion adverse "en passant" (voir la section [mises à jour](#mises-à-jour) pour plus de détails). Cette classe est accessible dans [piece.py](piece.py), ses sous-classes sont les suivantes : [pion.py](pion.py), [cavalier.py](cavalier.py), [tour.py](tour.py), [fou.py](fou.py), [dame.py](dame.py) et [roi.py](roi.py).

> __**Note**__ : le rock est disponible (lorsque légal) par un clic sur le roi de sa couleur.

### Classe ``Board``

C'est une sorte de sous classe de la classe game, en tant que contenue dans cette dernière. C'est aussi la classe qui contient toutes les pièces ainsi que la plupart des fonctions de dessins (la case sélectionnée, le dernier déplacement, le score, les joueurs, les cases disponibles pour déplacement, et d'autres pour n'en citer que quelques-unes). Elle est accessible dans le fichier [board.py](board.py).

### Classe ``Button`` et sous-classes

C'est la classe qui gèrera entre autres (voir la section [mises à jour](#mises-à-jour) pour plus de détails) la notion de "undo"/"redo". Le bouton "undo" fera du jeu actuel celui qui était affiché $n$ fois auparavant. Le bouton "redo" permet d'annuler un ou plusieurs appuis sur le précédent bouton. La classe générique est accessible dans [button.py](button.py) et ses sous-classes dans [undo.py](undo.py) et [redo.py](redo.py). Lors d'un appui sur un bouton, les différents états du jeu $-$**où le tour était à un joueur humain**, défilent. Lors de la reprise du jeu (lorsque le joueur clique sur le plateau), cet état devient l'état courant (il est rajouté à la fin de la liste des états) : il n'y a aucun état intermédiaire entre l'état "avant d'appuyer sur les boutons" et l'état "après avoir repris la partie", ce qui peut amener à un défilement du jeu étrange. Dans de prochaines mises à jour, et avec des retours, les états passés par les boutons seront supprimés (on reprend totalement le jeu $n$ étapes en arrière).

Cette classe gère aussi (à partir de la version 0.a06) la notion de pause. Les boutons pause et play sont disponibles dans [pause.py](pause.py) et [play.py](play.py). Lors de la pause, le jeu ne tourne plus qu'à un tick par seconde (par opposition à 60), et lors de la sortie de pause, il est donné un temps de 3 secondes avant que la partie ne reprenne.

### Classe ``Clock``

C'est une petite classe qui permet le suivi de la durée de jeu ainsi que la notion de chronomètre dans de futures mises à jour. La durée de jeu est affichée à la seconde, le chronomètre tant qu'à lui sera au dixième de seconde $-$une actualisation plus fréquente étant peu envisageable étant donné que le jeu tourne à 60 ticks par secondes (18ms).

## Librairies et autre prérequis

> __**Note**__ : il est recommendé d'avoir python >= 3.6.4, d'utiliser la dernière version de [pip](https://pypi.org/project/pip/) et des modules listés ci-après

-   [pygame](https://pypi.org/project/pygame/)
-   [numpy](https://pypi.org/project/numpy/)

Les librairies time et json devraient être installées par défaut avec python.

Il est aussi **impératif** d'installer las polices suivantes (les deux dernières devraient être installées par défaut):

-   [jetbrains Mono](https://www.jetbrains.com/lp/mono/)
-   Comic Sans MS (eh oui !)
-   Sans-Serif

## Mises à jour

À venir :

-   0.a10 : mise en fonctionnement des boutons "undo"/"redo"
-   0.b01 : mise en fonctionnement de l'ia

Prévues précédemment :

-   0.a04 : correction de bugs et accélération
-   0.a05 : détection du mat + fin de partie
-   0.a06 : ajout d'un bouton de pause
-   0.a09 : ajout de "en passant" pour les pions

## Changelog

-   0.a01 : première version, les pièces ne se déplacent pas ;
-   0.a02 : les pièces se déplacent, améliorations de l'interface utilisateur, ajout de boutons (pour le moment non fonctionnels) ;
-   0.a03 : le joueur mis en échec est forcé de quitter cet état par la restriction des coups disponibles, première version du calcul du score, inventaire des pièces mangées, overlay du dernier mouvement, création de [README.md](README.md) ;
-   0.a04 : calcul de l'état d'échec des joueurs uniquement lors d'un mouvement (i.e. lorsque l'on passe au joueur suivant), le joueur ne peut plus se mettre tout seul en échec, nouvelle formule de calcul de score, correction du bug où le score affiché était de -0.0 dû aux erreurs de calcul python, ajout de la durée de la partie ;
-   0.a05 : détection de l'échec-et-mat, lorsque la partie se termine les boutons restent accessibles mais aucun joueur ne peut déplacer de pièces, vérification des joueurs en début de partie (les deux joueurs doivent avoir des pièces de couleur différente), le tour de l'ia est lancé plus systématiquement ce qui devrait permettre à l'ordinateur de jouer contre lui-même ;
-   0.a06 : ajout d'un bouton de pause, mise en pause du timer pour la durée de la partie, ajout d'un compteur pour la sortie de pause ;
-   0.a07 : corrections de bugs, amélioration du calcul du score, affectation d'une valeur plus réaliste au roi ;
-   0.a08 : déplacement des tests de déplacement (si la pièce arrive sur une pièce ennemie, le test pour le rock, et autres) de la classe Human vers la classe Piece dans la fonction move_to() pour qu'ils soient utilisables plus facilement par l'ordinateur dans les versions *beta*, correction du bug où le pion pouvait avancer de deux cases en sortie de rangée alors que la première case n'était pas libre, ajout des librairies requises ;
-   0.a09 : ajout de "en passant" pour les pions ;
