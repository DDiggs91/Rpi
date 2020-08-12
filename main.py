import pygame

# Window 800x480
pygame.init()
DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPSCLOCK = pygame.time.Clock()
BIGFONT = pygame.font.SysFont(None, 80)
SMALLFONT = pygame.font.SysFont(None, 40)
while True:
    event_upkeep = []
    for event in pygame.event.get():
        event_upkeep.append(str(event))

    DISPLAY.fill((255, 0, 0))

    text = BIGFONT.render("{}".format(pygame.display.get_surface().get_size()), True, (0, 0, 0))
    DISPLAY.blit(text, (350, 350))

    text = SMALLFONT.render("{}".format(pygame.display.get_surface().get_size()), True, (0, 0, 0))
    DISPLAY.blit(text, (450, 450))

    pygame.display.update()
    FPSCLOCK.tick(60)
