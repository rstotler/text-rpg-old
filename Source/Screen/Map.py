import pygame
from pygame import *

class Map:

    def __init__(self):
        self.surface = pygame.Surface([200, 200])
        self.surface.fill([10, 30, 70])

    def draw(self, window):
        window.blit(self.surface, [600, 0])
