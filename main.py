import pygame
import math
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
    BIG_FONT = pygame.font.SysFont(None, min(WINDOW_WIDTH // 6, 80))
    SMALL_FONT = pygame.font.SysFont(None, max(WINDOW_WIDTH // 12, 40))

    mos_pos = [0, 0]
    mos_down = False

    slider_brightness = LightSliderControl(WINDOW_WIDTH * 1 // 16, WINDOW_HEIGHT * 6 // 8, WINDOW_WIDTH * 6 // 8,
                                           WINDOW_HEIGHT * 1 // 8, 16)

    hue_sat_control = CircleControl(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, WINDOW_HEIGHT // 4)

    all_controls = pygame.sprite.Group()
    all_controls.add(slider_brightness)
    all_controls.add(hue_sat_control)
    BACKGROUND_COLOR = [0, 0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mos_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and not mos_down:
                mos_down = True
                for sprite in all_controls:
                    sprite.clicked(mos_pos)
            elif event.type == pygame.MOUSEBUTTONUP and mos_down:
                mos_down = False
                for sprite in all_controls:
                    sprite.selected = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        DISPLAY.fill((100, 0, 0))
        all_controls.draw(DISPLAY)
        all_controls.update(mos_pos, mos_down)
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


class CircleButton(pygame.sprite.Sprite):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.rect = self.image.get_rect()
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, (120, 120, 120), (radius, radius), radius)


class CircleControl(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.x = x
        self.y = y
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.button = CircleButton(sorted([80, self.radius // 20, 8])[1])
        self.button.rect.center = (self.radius, self.radius)
        self.image.blit(self.button.image, self.button.rect.topleft)

        self.selected = False
        self.value = (0, 0)

    def update(self, mos_pos, mos_down, *kwargs):
        if self.selected and mos_down:
            r, theta = car_to_pol(mos_pos[0] - self.radius - self.rect.x, self.rect.y - (mos_pos[1] - self.radius))
            if r >= self.radius - self.button.radius:
                r = self.radius - self.button.radius
            self.value = (r, theta)
            x, y = pol_to_car(r, theta)
            self.button.rect.center = (x + self.radius, self.radius - y)
            self.button.update()

        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)

        self.image.blit(self.button.image, self.button.rect.topleft)

    def clicked(self, mos_pos):
        if self.rect.x + self.button.rect.x < mos_pos[0]:
            if mos_pos[0] < self.rect.x + self.button.rect.x + self.button.rect.width:
                if self.rect.y + self.button.rect.y < mos_pos[1]:
                    if mos_pos[1] < self.rect.y + self.button.rect.y + self.button.rect.height:
                        self.selected = True


class LightCircleControl(CircleControl):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.lights = bridge.lights
        self.bri = self.lights[0].brightness
        for light in self.lights:
            light.transition_time = 0

    def update(self, mos_pos, mos_down, *kwargs):
        super().update(mos_pos, mos_down, **kwargs)


class LightSliderControl(Slider):
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


class LightControl:
    def __init__(self, x, y, width, height):
        self.hue_sat_control = LightCircleControl(x, y, min(width, height))
        self.bri_control = LightSliderControl(width // 16, height, x, y)

    def update(self, mos_pos, mos_down):
        self.hue_sat_control.update(mos_pos, mos_down)
        self.bri_control.update(mos_pos, mos_down)

    def draw(self, surface):
        surface.blit(self.hue_sat_control.image)
        surface.blit(self.bri_control.image)



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


def car_to_pol(x, y):
    r = (x ** 2 + y ** 2) ** 0.5
    theta = math.degrees(math.atan2(y, x))
    if theta < 0:
        theta += 360
    return r, theta


def pol_to_car(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


if __name__ == '__main__':
    main()
