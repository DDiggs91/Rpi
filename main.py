import pygame

# Window 800x480
pygame.init()
DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = pygame.display.get_surface().get_size()
FPSCLOCK = pygame.time.Clock()
BIGFONT = pygame.font.SysFont(None, 80)
SMALLFONT = pygame.font.SysFont(None, 40)

mouse_pos = (0, 0)

while True:
    event_upkeep = []
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = [str(i) for i in event.pos}

    DISPLAY.fill((255, 0, 0))

    text = BIGFONT.render(','.join(mouse_pos), True, (0, 0, 0))
    DISPLAY.blit(text, (350, 350))

    pygame.display.update()
    FPSCLOCK.tick(60)
