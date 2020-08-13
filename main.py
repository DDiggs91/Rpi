import pygame
from platform import system
from phue import Bridge
from colorsys import hsv_to_rgb

b = Bridge('192.168.0.8')
b.connect()


def main():
    pygame.init()
    if system() == 'Linux':
        DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:  # system() == 'Windows':
        DISPLAY = pygame.display.set_mode((480, 270))
    WINDOWWIDTH, WINDOWHEIGHT = pygame.display.get_surface().get_size()
    FPSCLOCK = pygame.time.Clock()
    BIGFONT = pygame.font.SysFont(None, min(WINDOWWIDTH // 6, 80))
    SMALLFONT = pygame.font.SysFont(None, max(WINDOWWIDTH // 12, 40))

    mos_pos = [0, 0]
    mos_down = False

    slider_hue = LightControl(WINDOWWIDTH * 1 // 16, WINDOWHEIGHT * 6 // 8, WINDOWWIDTH * 2 // 8, WINDOWHEIGHT * 1 // 8,
                              16, 'hue')
    slider_saturation = LightControl(WINDOWWIDTH * 1 // 16, WINDOWHEIGHT * 6 // 8, WINDOWWIDTH * 4 // 8,
                                     WINDOWHEIGHT * 1 // 8, 16, 'saturation')
    slider_brightness = LightControl(WINDOWWIDTH * 1 // 16, WINDOWHEIGHT * 6 // 8, WINDOWWIDTH * 6 // 8,
                                     WINDOWHEIGHT * 1 // 8, 16, 'brightness')

    all_sliders = pygame.sprite.Group()
    all_sliders.add(slider_hue)
    all_sliders.add(slider_saturation)
    all_sliders.add(slider_brightness)
    BACKGROUND_COLOR = [int(i * 255) for i in hsv_to_rgb(b.lights[0].hue / 65535 * 360, b.lights[0].saturation / 255,
                                                         b.lights[0].brightness / 255)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mos_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and not mos_down:
                mos_down = True
                for sprite in all_sliders:
                    sprite.clicked(mos_pos)
            elif event.type == pygame.MOUSEBUTTONUP and mos_down:
                mos_down = False
                for sprite in all_sliders:
                    sprite.selected = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        DISPLAY.fill(BACKGROUND_COLOR)
        all_sliders.draw(DISPLAY)
        all_sliders.update(mos_pos, mos_down)
        pygame.display.update()
        FPSCLOCK.tick(60)


class SliderButton(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill((120, 120, 120))


class Slider(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, divisions):
        super().__init__()
        self.image = pygame.Surface([round(width / divisions) * divisions, round(height / divisions) * divisions])
        self.image.fill((192, 192, 192))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.div = divisions
        pygame.draw.line(self.image, (0, 0, 0), (self.rect.width // 2, self.rect.height * 1 // self.div),
                         (self.rect.width // 2, self.rect.height * (self.div - 1) // self.div),
                         max(self.rect.width * 1 // self.div, 1))
        self.button = SliderButton(self.rect.width, self.rect.height * 1 // self.div)
        self.button.rect.topleft = (0, self.rect.height * (self.div // 2 - 1) // 16)
        self.image.blit(self.button.image, self.button.rect.topleft)
        self.selected = False
        self.oldvalue = 0
        self.value = 0

    def update(self, mos_pos, mos_down, *kwargs):
        if self.selected and mos_down:
            self.value = sorted([1, (mos_pos[1] - self.rect.y) // (self.rect.height // self.div), self.div - 1])[1]
            self.button.rect.centery = self.value * (self.rect.height // self.div)
            self.button.update()

        self.image.fill((192, 192, 192))
        pygame.draw.line(self.image, (0, 0, 0), (self.rect.width // 2, self.rect.height * 1 // self.div),
                         (self.rect.width // 2, self.rect.height * (self.div - 1) // self.div),
                         max(self.rect.width * 1 // self.div, 1))
        for i in range(1, self.div):
            pygame.draw.line(self.image, (0, 0, 0), (
                self.rect.width * (self.div // 4 - 1) // (self.div // 2), i * self.rect.height // self.div),
                             (self.rect.width * (self.div // 4 + 1) // (self.div // 2),
                              i * self.rect.height // self.div))
        self.image.blit(self.button.image, self.button.rect.topleft)

    def clicked(self, mos_pos):
        if self.rect.x + self.button.rect.x < mos_pos[0]:
            if mos_pos[0] < self.rect.x + self.button.rect.x + self.button.rect.width:
                if self.rect.y + self.button.rect.y < mos_pos[1]:
                    if mos_pos[1] < self.rect.y + self.button.rect.y + self.button.rect.height:
                        self.selected = True


class LightControl(Slider):
    def __init__(self, width, height, x, y, divisions, mode):
        super().__init__(width, height, x, y, divisions)
        self.mode = mode
        self.lights = b.lights
        for l in self.lights:
            l.transitiontime = 0

    def update(self, mos_pos, mos_down, *kwargs):
        super().update(mos_pos, mos_down, *kwargs)
        if self.value != self.oldvalue:
            self.oldvalue = self.value
            light_value = self.div - (self.value + 1)
            if self.mode == 'hue':
                for l in self.lights:
                    l.hue = light_value * 65535 // self.div
            elif self.mode == 'saturation':
                for l in self.lights:
                    l.saturation = light_value * 254 // self.div
            elif self.mode == 'brightness':
                if light_value == 0:
                    for l in self.lights:
                        l.on = False
                else:
                    for l in self.lights:
                        if not l.on:
                            l.on = True
                        l.brightness = light_value * 254 // self.div
            BACKGROUND_COLOR = [int(i * 255) for i in
                                hsv_to_rgb(b.lights[0].hue / 65535 * 360, b.lights[0].saturation / 255,
                                           b.lights[0].brightness / 255)]


if __name__ == '__main__':
    main()
