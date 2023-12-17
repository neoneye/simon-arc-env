import os
import pygame

class Cursors:
    def __init__(self, scale: int):
        self.scale = scale

        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "assets", "arrow_right.png")

        raw_image = pygame.image.load(path)
        self.arrow_right_image = pygame.transform.scale(raw_image, (scale - 1, scale - 1))
        self.arrow_down_image = pygame.transform.rotate(self.arrow_right_image, 270)

    def draw(self, surface: pygame.Surface, cursor_x: int, cursor_y: int) -> None:
        s = self.scale

        # cursor x
        ax = (cursor_x + 1) * s
        ay = 0

        # cursor y
        bx = 0
        by = (cursor_y + 1) * s

        if s > 6:
            surface.blit(self.arrow_down_image, (ax, ay))
            surface.blit(self.arrow_right_image, (bx, by))
        else:
            pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(ax, ay, s, s))
            pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(bx, by, s, s))
