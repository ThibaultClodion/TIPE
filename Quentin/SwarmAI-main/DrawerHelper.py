import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import os
from pygame.locals import *


class DrawerHelper:
    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (255, 122, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    TEAL = (0, 80, 80)

    def __init__(self, title, width, height):
        # set up pygame
        pygame.init()
        # set up the window
        pygame.display.set_caption(title)
        self.windowSurface = pygame.display.set_mode((width, height), 0, 32)
        self.windowSurface.fill(self.WHITE)

    def draw_background(self, color):
        self.windowSurface.fill(color)

    def draw_line(self, color, pos_1, pos_2, width=1):
        pygame.draw.line(self.windowSurface, color, pos_1, pos_2, width)

    def draw_point(self, color, pos, width=1):
        pygame.draw.line(self.windowSurface, color, pos, pos, width)

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.windowSurface, color, rect)

    def draw_ellipse(self, color, rect, width=1):
        pygame.draw.ellipse(self.windowSurface, color, rect, width)

    def draw_circle(self, color, center, radius,  width=1):
        pygame.draw.ellipse(self.windowSurface, color, center, radius, width)

    def draw_polygon(self, color, points, width=1):
        pygame.draw.polygon(self.windowSurface, color, points, width)

    def blit(self, color, alpha, x, y, scale):
        s = pygame.Surface((scale, scale))
        s.set_alpha(alpha)
        s.fill(color)
        self.windowSurface.blit(s, (x * scale, y * scale))

    def draw_arc(self, color, rect, start_angle, end_angle):
        pygame.draw.arc(self.windowSurface, color, rect, start_angle, end_angle)

    def get_window_surface(self):
        return self.windowSurface

    def load_image(self, file):
        return pygame.image.load(os.path.join('assets', file))

    def draw_image(self, image, pos):
        image_rect = image.get_rect(center=pos)
        self.windowSurface.blit(image, image_rect)
        pygame.display.flip()

    def scale_image(self, image, size):
        return pygame.transform.scale(image, size)
