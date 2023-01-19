import os
import sys
import random

import pygame

pygame.init()
size = width, height = 600, 200
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dino(pygame.sprite.Sprite):
    image_run = load_image("Dino_run.png")
    image_jump = load_image("Dino_J.png")
    image_down = load_image("Dino_down.png")
    image_fail = load_image("Dino_F.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.cut_sheet(Dino.image_run, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, count):
        self.frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // count, sheet.get_height())
        self.rect.x = 20
        self.rect.y = 160 - sheet.get_height()
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self, *args):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if pygame.sprite.spritecollideany(self, cacti):
            self.image = self.image_fail

        for e in args:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.cut_sheet(self.image_jump, 1)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.cut_sheet(self.image_down, 2)
            if e.type == pygame.KEYUP:
                self.cut_sheet(self.image_run, 2)


class Cactus(pygame.sprite.Sprite):
    image = load_image("Cactus.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Cactus.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = 110

    def update(self, *args):
        self.rect = self.rect.move(-5, 0)


class Cloud(pygame.sprite.Sprite):
    image = load_image("Cloud.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Cloud.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.randrange(30, 70)

    def update(self, *args):
        self.rect = self.rect.move(-2, 0)


if __name__ == '__main__':
    dino = pygame.sprite.Group()
    cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    Dino(dino)
    Cloud(clouds)

    fps = 30
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1500)
    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (100, 100, 100), (0, 150), (width, 150), 2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                dino.update(event)
            if event.type == pygame.USEREVENT:
                #for _ in range(random.randrange(1, 3)):
                Cactus(cacti)
                pygame.time.set_timer(pygame.USEREVENT, random.randrange(1500, 3500))
            if event.type == pygame.USEREVENT + 1:
                Cloud(clouds)


        # Каждые n секунд рисовать кактусы (группами от 1 до 3 и облака)

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (100, 100, 100), (0, 150), (width, 150), 1)
        dino.draw(screen)
        cacti.draw(screen)
        clouds.draw(screen)
        dino.update()
        cacti.update()
        clouds.update()

        clock.tick(fps)
        pygame.display.flip()
