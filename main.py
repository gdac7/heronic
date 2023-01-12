
# Up level in enemies

import pygame
import sys
from random import randint, choice


def set_timer(enemy_spawn, t):
    pygame.time.set_timer(enemy_spawn, t)


def check_collision(hero_group, enemies_group):
    enemy_collided = pygame.sprite.spritecollide(hero_group.sprite, enemies_group, False)
    for enemy in enemy_collided:
        if enemy.__repr__() == 'baby_dragon':
            if enemy.rect.x < hero_group.sprite.rect.x:
                if abs(enemy.rect.x - hero_group.sprite.rect.x) <= 30:
                    return False
            elif enemy.rect.x > hero_group.sprite.rect.x:
                if abs(enemy.rect.x - hero_group.sprite.rect.x) <= 50:
                    return False
        else:
            if enemy.rect.x < hero_group.sprite.rect.x:
                if enemy.rect.x < 0:
                    if abs(enemy.rect.y - hero_group.sprite.rect.y) <= 5:
                        return False
                else:
                    if abs(enemy.rect.x - hero_group.sprite.rect.x) <= 50 and abs(enemy.rect.y - hero_group.sprite.rect.y) <= 30:
                        return False
            elif enemy.rect.x > hero_group.sprite.rect.x:
                if abs(enemy.rect.x - hero_group.sprite.rect.x) <= 50 and abs(enemy.rect.y - hero_group.sprite.rect.y) <= 30:
                    return False

    return True


def show_score_and_level(score, screen, score_font, current_level, level_font):
    score_text = score_font.render(f"Score : {score}", True, "yellow")
    score_rect = score_text.get_rect(center=(380, 15))
    level_text = level_font.render(f"Level : {current_level + 1}", True, "red")
    level_text_rect = level_text.get_rect(center=(380, 40))
    screen.blit(score_text, score_rect)
    screen.blit(level_text, level_text_rect)


def change_screen(screen, button, button_rect, ext, ext_rect, text, text_rect, state):
    if state == 'start':
        screen.fill("black")
        screen.blit(text, text_rect)
        screen.blit(button, button_rect)
        screen.blit(ext, ext_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif ext_rect.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()
    else:
        screen.fill("black")
        screen.blit(text, text_rect)
        screen.blit(button, button_rect)
        screen.blit(ext, ext_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif ext_rect.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.image.load("hero/run1.png").convert_alpha(),
            pygame.image.load("hero/run2.png").convert_alpha(),
            pygame.image.load("hero/run3.png").convert_alpha(),
            pygame.image.load("hero/run4.png").convert_alpha(),
            pygame.image.load("hero/run5.png").convert_alpha(),
            pygame.image.load("hero/run6.png").convert_alpha(),
            pygame.image.load("hero/run7.png").convert_alpha(),
        ]
        self.player_jump_up = pygame.image.load("hero/jump_up.png").convert_alpha()
        self.player_jump_down = pygame.image.load("hero/jump_down.png").convert_alpha()
        self.jump_sound = [pygame.mixer.Sound("hero/jump/jump1.ogg"), pygame.mixer.Sound("hero/jump/jump2.ogg")]
        self.rect = self.frames[0].get_rect(bottom=340)
        self.rect.x = 100
        self.initial_y = self.rect.y
        self.gravity = 0
        self.frame_index = 0
        self.score = 0
        self.image = self.frames[self.frame_index]

    def simulate_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.y >= self.initial_y:
            self.rect.y = self.initial_y

    def get_jump(self):
        sound = choice(self.jump_sound)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.y == self.initial_y:
            sound.play()
            self.gravity = -20

    def animate(self):
        if self.rect.y == self.initial_y:
            self.frame_index += 0.2
            if self.frame_index >= 7:
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
        else:
            if self.gravity < 0:
                self.image = self.player_jump_up
            else:
                self.image = self.player_jump_down



    def update(self):
        self.simulate_gravity()
        self.get_jump()
        self.animate()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, frames: list, name, speed):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.name = name
        if self.name == 'baby_dragon':
            self.rect = self.frames[0].get_rect(bottom=350)
        if self.name == 'dragon':
            self.rect = self.frames[0].get_rect(bottom=180)
        self.rect.x = randint(850, 1100)
        self.image = self.frames[self.frame_index]
        self.speed = speed
        self.increased = False

    def __repr__(self):
        if self.name == 'baby_dragon':
            return 'baby_dragon'
        else:
            return 'dragon'

    def animate(self):
        self.frame_index += 0.1
        if self.name == 'baby_dragon':
            if self.frame_index >= 5:
                self.frame_index = 0
        if self.name == 'dragon':
            if self.frame_index >= 3:
                self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def destructor(self):
        if self.__repr__() == 'baby_dragon':
            if self.rect.x < -50:
                self.kill()
        else:
            if self.rect.x < -100:
                self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.animate()
        self.destructor()


def main():
    score = 0
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('HERONIC')
    score_font = pygame.font.Font("font/font1.ttf", 30)
    level_font = pygame.font.Font("font/font1.ttf", 15)
    baby_dragon_frames = [
        pygame.image.load("babydragon/walk1.png").convert_alpha(),
        pygame.image.load("babydragon/walk2.png").convert_alpha(),
        pygame.image.load("babydragon/walk3.png").convert_alpha(),
        pygame.image.load("babydragon/walk4.png").convert_alpha(),
        pygame.image.load("babydragon/walk5.png").convert_alpha(),
    ]
    dragon_frames = [
        pygame.image.load("dragon/fly1.png").convert_alpha(),
        pygame.image.load("dragon/fly2.png").convert_alpha(),
        pygame.image.load("dragon/fly3.png").convert_alpha()
    ]
    start_button = pygame.image.load("buttons/start_button.png").convert_alpha()
    sb_rect = start_button.get_rect(center=(380, 250))

    continue_button = pygame.image.load("buttons/continue_button.png").convert_alpha()
    cb_rect = continue_button.get_rect(center=(380, 250))

    exit_button = pygame.image.load("buttons/exit_button.png").convert_alpha()
    eb_rect = exit_button.get_rect(center=(380, 325))

    start_font = pygame.font.Font("font/font1.ttf", 50)
    game_text = start_font.render("Heronic", True, "blue")
    game_text_rect = game_text.get_rect(center=(380, 50))

    clock = pygame.time.Clock()
    background_img = pygame.image.load("images/desert_BG.png").convert_alpha()
    hero = pygame.sprite.GroupSingle()
    hero.add(Hero())
    enemies_group = pygame.sprite.Group()
    enemies_speed = 5

    levels = [1300, 1150, 1000, 850, 500]
    current_level = 0
    enemy_spawn = pygame.event.custom_type()
    set_timer(enemy_spawn, levels[current_level])
    increase_score = pygame.event.custom_type()
    pygame.time.set_timer(increase_score, 1500)

    spawn_list = ['baby_dragon', 'baby_dragon', 'baby_dragon', 'dragon']
    game_on = change_screen(screen, start_button, sb_rect, exit_button, eb_rect, game_text, game_text_rect, 'start')
    game_song = pygame.mixer.Sound('game_song.ogg')
    game_song.set_volume(0.1)
    game_song.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if game_on:
                if event.type == enemy_spawn:
                    if choice(spawn_list) == 'baby_dragon':
                        enemies_group.add(Enemy(baby_dragon_frames, 'baby_dragon', enemies_speed))
                    else:
                        enemies_group.add(Enemy(dragon_frames, 'dragon', enemies_speed))
                if event.type == increase_score:
                    score += 1
                    if score % 10 == 0 and current_level <= 3:
                        enemies_speed += 1
                        current_level += 1
                        set_timer(enemy_spawn, levels[current_level])

        if game_on:
            screen.blit(background_img, (0, 0))
            game_on = check_collision(hero, enemies_group)
            enemies_group.draw(screen)
            enemies_group.update()
            hero.draw(screen)
            hero.update()
            show_score_and_level(score, screen, score_font, current_level, level_font)
        else:
            game_song.stop()
            lose_text = start_font.render(f"Your score: {score}", True, "yellow")
            lose_text_rect = lose_text.get_rect(center=(380, 50))
            game_on = change_screen(screen, continue_button, cb_rect, exit_button, eb_rect, lose_text, lose_text_rect, 'lose')
            if game_on:
                enemies_group.empty()
                score = 0
                current_level = 0
                enemies_speed = 5
                game_song.play(loops=-1)

        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
