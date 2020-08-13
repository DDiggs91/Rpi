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
    slider1 = Slider(WINDOWWIDTH * 1 // 16, WINDOWHEIGHT * 6 // 8, WINDOWWIDTH * 2 // 8, WINDOWHEIGHT * 1 // 8)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(slider1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        DISPLAY.fill((255, 0, 0))
        all_sprites.draw(DISPLAY)
        all_sprites.update()
        pygame.display.update()
        FPSCLOCK.tick(60)

class SliderButton(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()


class Slider(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((192, 192, 192))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        pygame.draw.line(self.image, (0, 0, 0), (self.rect.width // 2, self.rect.height * 1 // 16),
                         (self.rect.width // 2, self.rect.height * 15 // 16), self.rect.width * 1 // 16)


if __name__ == '__main__':
    main()
