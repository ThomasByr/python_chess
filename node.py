import numpy as np


class Node:
    def __init__(
        self, color: str, parent, board: np.array, move: tuple({tuple({int})})
    ):
        """
        une classe d'arbre pour l'ia
        
        Parameters
        ----------
            color : str
                la couleur du joueur lors du coup
            parent : Node
                le noeud parent
            board : np.array
                le plateau de jeu
            move : tuple
                les coordonnées du déplacement pour arriver du parent.board à self.board
                (from_index, to_index)
        """
        self.value = None
        self.board = board
        self.move = move
        self.color = color
        self.parent = parent
        self.list_of_leaves = []

    def __repr__(self):
        print(self.board)
        for child in self.list_of_leaves:
            print(child)

    def __append__(self, other):
        """
        ajoute un arbre
        
        Parameters
        ----------
            other : Tree
                l'arbre à ajouter
        """
        self.list_of_leaves.append(other)

    def get_size(self) -> int:
        """
        le nombre de feuilles
        """
        res = 0
        for child in self.list_of_leaves:
            res += child.get_size()
        return 1 + res

    def get_height(self) -> int:
        """
        la hauteur de l'arbre
        """
        res = []
        for child in self.list_of_leaves:
            res.append(child.get_height())
        if res == []:
            return 0
        return 1 + max(res)

    def get_all_last(self) -> list:
        """
        donne tous les éléments de dernier niveau
        """
        res = []
        if self.list_of_leaves[0].list_of_leaves == []:
            res.extend(self.list_of_leaves)
        else:
            for child in self.list_of_leaves:
                res.extend(child.get_all_last())
        return res

    def get_values(self, fun) -> float:
        """
        donne la valeur à tous les noeuds
        
        Parameters
        ----------
            fun : <class 'function'>
                une fonction de poids
        Returns
        -------
            float : valeur
        """

        if self.list_of_leaves == []:
            self.value = fun(self.board)

        vals = []
        for child in self.list_of_leaves:
            if child.value is None:
                child.get_values(fun)
            vals.append(child.value)

        if self.list_of_leaves != []:
            if self.color == "n":
                self.value = min(vals)
            if self.color == "b":
                self.value = max(vals)
