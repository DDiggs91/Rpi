import pygame
import platform

# Window 800x480
pygame.init()
print(platform.system())
quit()
if platform.system() == 'Windows':
    DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
elif platform.system() ==
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
            mouse_pos = [str(i) for i in event.pos]

    DISPLAY.fill((255, 0, 0))

    text = BIGFONT.render(','.join(mouse_pos), True, (0, 0, 0))
    DISPLAY.blit(text, (WINDOWWIDTH // 2, WINDOWHEIGHT // 2))

    pygame.display.update()
    FPSCLOCK.tick(60)
