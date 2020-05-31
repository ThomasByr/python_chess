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
                ce que fait ce bouton : 1 = undo | 2 = redo
        """
        self.image = pygame.image.load(f"images/flêche{action}.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (20, 11))
