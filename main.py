import pygame

# Window 800x600
screen = (800, 600)
pygame.init()
DISPLAY = pygame.display.set_mode(screen, pygame.FULLSCREEN)
FPSCLOCK = pygame.time.Clock()
while True:
    DISPLAY.fill((255, 0, 0))
    pygame.display.flip()
    FPSCLOCK.tick()
