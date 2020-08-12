import pygame

# Window 800x480
pygame.init()
DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPSCLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 80)
while True:
    event_upkeep = []
    for event in pygame.event.get():
        event_upkeep.append(str(event))

    DISPLAY.fill((255, 0, 0))

    text = FONT.render(','.join(event_upkeep), True, (0, 0, 0))
    DISPLAY.blit(text, (250, 250))

    text2 = FONT.render("{}".format(pygame.display.get_surface().get_size()), True, (0, 0, 0))
    DISPLAY.blit(text2, (350, 350))
    pygame.display.update()
    FPSCLOCK.tick(60)
