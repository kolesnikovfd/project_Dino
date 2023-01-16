import os
import sys
import random

import pygame

pygame.init()
size = width, height = 435, 200
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
    image_run_L = load_image("Dino_L.png")
    image_run_R = load_image("Dino_R.png")
    image_jump = load_image("Dino_J.png")
    image_bend = load_image("Dino_DL.png")
    image_fail = load_image("Dino_F.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Dino.image_jump
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 120

    def update(self, *args):
        if self.image == self.image_run_L:
            self.image = self.image_run_R
        else:
            self.image = self.image_run_L
        if args:
            if args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_SPACE:
                self.image = self.image_jump


class Cactus(pygame.sprite.Sprite):
    image = load_image("Cactus.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Cactus.image
        self.rect = self.image.get_rect()
        self.rect.x = width - 1
        self.rect.y = 120

    def update(self, *args):
        self.rect = self.rect.move(-1, 0)



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
        self.rect = self.rect.move(-0.5, 0)


if __name__ == '__main__':
    dino = pygame.sprite.Group()
    cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    Dino(dino)
    Cactus(cacti)

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (100, 100, 100), (0, 150), (width, 150), 2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                dino.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                Cactus(cacti)

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (100, 100, 100), (0, 150), (width, 150), 2)
        dino.draw(screen)
        dino.update()
        pygame.display.flip()
