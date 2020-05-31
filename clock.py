import time


class Clock:
    def __init__(self, max_time: int, increment: int):
        """
        classe d'horloge
        
        Parameters
        ----------
            max_time : int
                le temps maximum dont dispose le joueur pour jouer son coup
                entrer -1 pour désactiver cette fonction
            increment : int
                le nombre de secondes à ajouter lorsque le joueur à fini son tour
                ne fonctionne que si max_time != -1
        """
        self.start = time.time()  # le temps courant en secondes
        self.max_time = max_time  # le temps max en secondes
        self.increment = increment  # le nombre de secondes à ajouter

    def get_time(self) -> tuple({int}):
        """
        fonction chronomètre pour avoir la durée de la partie en cours
        
        Returns
        -------
            tuple : le temps en h/m/s
        """
        h, m, s = 0, 0, 0  # heures/minutes/secondes
        cur = time.time() - self.start  # le temps écoulé en secondes
        h = cur // (60 * 60)
        cur -= h * 60 * 60
        m = cur // 60
        cur -= m * 60
        s = cur
        return int(h), int(m), int(s)

    def get_time_in_sec(self) -> float:
        return time.time() - self.start

    def reset(self, new_start):
        self.start = time.time() - new_start
