import pygame
from pygame import *
from Game import Game

pygame.init()
pygame.display.set_caption("Universe")
window = pygame.display.set_mode((800, 600), 0, 32)
clock = pygame.time.Clock()
game = Game()

while True:
    clock.tick(60)
    game.update(window, str(int(clock.get_fps())))
    pygame.display.flip()
