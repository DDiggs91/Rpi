import pygame
from platform import system
from phue import Bridge

bridge = Bridge('192.168.0.8')
bridge.connect()


def main():
    pygame.init()
    if system() == 'Linux':
        DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:  # system() == 'Windows':
        DISPLAY = pygame.display.set_mode((480, 270))
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
    FPS_CLOCK = pygame.time.Clock()
    BIGFONT = pygame.font.SysFont(None, min(WINDOW_WIDTH // 6, 80))
    SMALLFONT = pygame.font.SysFont(None, max(WINDOW_WIDTH // 12, 40))

    mos_pos = [0, 0]
    mos_down = False

    slider_brightness = LightControl(WINDOW_WIDTH * 1 // 16, WINDOW_HEIGHT * 6 // 8, WINDOW_WIDTH * 6 // 8,
                                     WINDOW_HEIGHT * 1 // 8, 16)

    all_sliders = pygame.sprite.Group()
    all_sliders.add(slider_brightness)
    BACKGROUND_COLOR = [0, 0, 0]

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
        DISPLAY.fill((0, 0, 0))
        all_sliders.draw(DISPLAY)
        all_sliders.update(mos_pos, mos_down)
        pygame.display.update()
        FPS_CLOCK.tick(60)


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
        self.old_value = 0
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
    def __init__(self, width, height, x, y, divisions):
        super().__init__(width, height, x, y, divisions)
        self.lights = bridge.lights
        self.bri = self.lights[0].brightness
        for light in self.lights:
            light.transition_time = 0

    def update(self, mos_pos, mos_down, *kwargs):
        super().update(mos_pos, mos_down, *kwargs)
        if self.value != self.old_value:
            self.old_value = self.value
            light_value = self.div - self.value - 1
            if light_value == 0:
                for light in self.lights:
                    self.bri = 0
                    light.brightness = 0
                    light.on = False
            else:
                self.bri = light_value * 255 // (self.div - 2)
                for light in self.lights:
                    if not light.on:
                        light.on = True
                    light.brightness = self.bri


def hsb_to_rgb(h, s, b):
    h = h
    s = s
    b = b
    C = b * s
    X = C * (1 - abs(h / 60 % 2 - 1))
    m = b - C
    if h < 60:
        (r, g, b) = (C, X, 0)
    elif h < 120:
        (r, g, b) = (X, C, 0)
    elif h < 180:
        (r, g, b) = (0, C, X)
    elif h < 240:
        (r, g, b) = (0, X, C)
    elif h < 300:
        (r, g, b) = (X, 0, C)
    else:
        (r, g, b) = (C, 0, X)
    (r, g, b) = ((r + m) * 255, (g + m) * 255, (b + m) * 255)
    return int(r), int(g), int(b)


if __name__ == '__main__':
    main()
