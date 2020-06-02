import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self):
        """
        classe générique
        """
        super().__init__()
        self.action = 0
        self.game = None

    def get_image(self, action: int):
        """
        donne l'image à un bouton
        
        Parameters
        ----------
            action : int
                ce que fait ce bouton
                1 = help | 2 = surrender | 3 = pause | 4 = play
        """
        self.image = pygame.image.load(f"images/bouton{action}.png")
        self.rect = self.image.get_rect()
