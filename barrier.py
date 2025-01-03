import pygame


class Barrier:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

    def blocks(self, x, y):
        """Sprawdza, czy punkt jest w barierze."""
        if self.rect.collidepoint(x, y):
            inter_x = max(self.rect.left, min(x, self.rect.right))
            inter_y = max(self.rect.top, min(x, self.rect.bottom))
            return True, (inter_x, inter_y)
        return False, None
