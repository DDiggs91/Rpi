import pygame
from platform import system


def main():
    pygame.init()
    if system() == 'Linux':
        DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        SCALEFACTOR = 1
    else:  # system() == 'Windows':
        DISPLAY = pygame.display.set_mode((480, 270))
        SCALEFACTOR = .25
    WINDOWWIDTH, WINDOWHEIGHT = pygame.display.get_surface().get_size()
    FPSCLOCK = pygame.time.Clock()
    BIGFONT = pygame.font.SysFont(None, int(80 * SCALEFACTOR))
    SMALLFONT = pygame.font.SysFont(None, int(40 * SCALEFACTOR))

    mouse_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        DISPLAY.fill((255, 0, 0))

        pygame.display.update()
        FPSCLOCK.tick(60)


if __name__ == '__main__':
    main()
