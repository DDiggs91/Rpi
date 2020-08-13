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

    mos_pos = [0, 0]
    mos_down = False

    slider1 = Slider(WINDOWWIDTH * 1 // 16, WINDOWHEIGHT * 6 // 8, WINDOWWIDTH * 2 // 8, WINDOWHEIGHT * 1 // 8)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(slider1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mos_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and not mos_down:
                mos_down = True
                for sprite in all_sprites:
                    sprite.clicked(mos_pos)
            elif event.type == pygame.MOUSEBUTTONUP and mos_down:
                mos_down = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        DISPLAY.fill((255, 0, 0))
        all_sprites.draw(DISPLAY)
        all_sprites.update(mos_pos, mos_down)
        pygame.display.update()
        FPSCLOCK.tick(60)


class SliderButton(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill((120, 120, 120))

    def update(self, mos_pos, mos_down):
        pass


class Slider(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((192, 192, 192))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        pygame.draw.line(self.image, (0, 0, 0), (self.rect.width // 2, self.rect.height * 1 // 16),
                         (self.rect.width // 2, self.rect.height * 15 // 16), self.rect.width * 1 // 16)
        self.button = SliderButton(self.rect.width, self.rect.height * 1 // 16)
        self.button.rect.topleft = (0, self.rect.height * 7 // 16)
        self.image.blit(self.button.image, self.button.rect.topleft)
        self.selected = False

    def update(self, mos_pos, mos_down):
        self.button.update(mos_pos, mos_down)

    def clicked(self, mos_pos):
        if self.rect.x + self.button.rect.x < mos_pos[0]:
            if mos_pos[0] < self.rect.x + self.button.rect.x + self.button.rect.width:
                if self.rect.y + self.button.rect.y < mos_pos[1]:
                    if mos_pos[1] < self.rect.y + self.button.rect.y + self.button.rect.height:
                        self.selected = True
                        print('clicked')


if __name__ == '__main__':
    main()
