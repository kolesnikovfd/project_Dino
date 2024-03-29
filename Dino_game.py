import os
import sys
import random

import pygame

pygame.init()
size = width, height = 600, 200
screen = pygame.display.set_mode(size)
pygame.display.set_caption('DINO')
all_sprites = pygame.sprite.Group()
font_path = 'data/Font.ttf'
sound_jump = pygame.mixer.Sound("data/Sound_jump.wav")
sound_score = pygame.mixer.Sound("data/Sound_score.wav")
sound_fail = pygame.mixer.Sound("data/Sound_fail.wav")
pygame.mixer.music.load('data/PHONK.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()
music_paused = True
with open('data/high_score.txt', 'r') as f:
    high_score = int(f.readline())


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

    def __init__(self):
        super().__init__(all_sprites)
        self.cut_sheet(Dino.image_run, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.is_jump = False
        self.jump_count = 10  # speed

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
        if not self.is_jump:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
            if args:
                e = args[0]
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and not self.is_jump:
                    self.image = self.image_jump
                    self.is_jump = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                    self.cut_sheet(self.image_down, 2)
                if e.type == pygame.KEYUP and not self.is_jump:
                    self.cut_sheet(self.image_run, 2)
        if self.is_jump:  # speed
            if self.jump_count == 10:
                sound_jump.play()
            if self.jump_count >= -10:
                if self.jump_count < 0:
                    self.rect.y += (self.jump_count ** 2) // 4
                else:
                    self.rect.y -= (self.jump_count ** 2) // 4
                self.jump_count -= 1
            else:
                self.jump_count = 10
                if not pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.is_jump = False


class Cactus(pygame.sprite.Sprite):
    images = [load_image(f"Cactus{i}.png") for i in range(1, 7)]

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cactus.images[random.randrange(6)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = 160 - self.image.get_height()

    def update(self, *args):
        global running
        self.rect.x -= 10  # speed
        if pygame.sprite.collide_mask(self, dino):
            running = False
            dino.image = dino.image_fail


class Bird(pygame.sprite.Sprite):
    image = load_image("Bird.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.cut_sheet(Bird.image, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.choice([75, 95, 115])  # random height

    def cut_sheet(self, sheet, count):
        self.frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() //
                                count, sheet.get_height())
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self, *args):
        global running
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x -= 10  # speed
        if pygame.sprite.collide_mask(self, dino):
            running = False
            dino.image = dino.image_fail


class Cloud(pygame.sprite.Sprite):
    image = load_image("Cloud.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cloud.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = random.randrange(30, 80)

    def update(self, *args):
        self.rect.x -= 1  # speed


def terminate():
    with open('data/high_score.txt', 'w') as f:
        f.write(str(high_score))
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["DINO GAME", "",
                  "Чтобы начать игру",
                  "Нажмите любую кнопку"]

    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('fon.png'), (width - 200, height))
    screen.blit(fon, (200, 0))
    font = pygame.font.Font(font_path, 20)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, False, (100, 100, 100))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


def restart_screen():
    font = pygame.font.Font(font_path, 30)
    text = font.render('Начать заново?', False, (100, 100, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return True  # начинаем игру
        pygame.display.flip()


def level():
    global dino, all_sprites, running, high_score, music_paused
    all_sprites = pygame.sprite.Group()
    dino = Dino()
    Cloud()
    score = 0

    # speed
    fps = 60
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    pygame.time.set_timer(pygame.USEREVENT + 1, 6000)

    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (100, 100, 100), (0, 153), (width, 153), 1)
    sand = [(random.randrange(width), random.randrange(157, 162)) for _ in range(20)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                music_paused = not music_paused
                if music_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.KEYUP:
                all_sprites.update(event)
            if event.type == pygame.USEREVENT:
                if score % 1000 > 500:
                    if random.randint(0, 1):
                        Bird()
                    else:
                        Cactus()
                else:
                    Cactus()
                pygame.time.set_timer(
                    pygame.USEREVENT, random.randrange(500, 1250))  # speed
            if event.type == pygame.USEREVENT + 1:
                Cloud()
                pygame.time.set_timer(pygame.USEREVENT + 1, random.randrange(2000, 5000))

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (100, 100, 100), (0, 153), (width, 153), 1)
        for i, pos in enumerate(sand):
            pygame.draw.line(screen, (100, 100, 100), pos, (pos[0] + 2, pos[1]), 1)
            sand[i] = ((pos[0] - 10) % width, pos[1])
        all_sprites.update()
        all_sprites.draw(screen)

        score += 1  # speed
        font = pygame.font.Font(font_path, 15)
        text = font.render(f'HI {high_score:06} {score:06}', False, (100, 100, 100))
        text_x = width - width // 4
        text_y = height // 20
        screen.blit(text, (text_x, text_y))
        if score % 500 == 0:
            sound_score.play()

        clock.tick(fps)  # speed
        pygame.display.flip()

        if not running:
            sound_fail.play()
            if high_score < score:
                high_score = score
            if restart_screen():
                level()


if __name__ == '__main__':
    start_screen()
    level()
