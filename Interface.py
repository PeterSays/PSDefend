import os
import random

import pygame.image
import pygame.font

pygame.font.init()

class Interface:
    def __init__(self, name, x, y, spritename, is_text=False, animation=None, text_value='', fontsize=24, fontcolor=(0, 0, 0)):
        self.name = name
        self.x = x
        self.y = y
        self.x_offset = 0
        self.y_offset = 0
        self.visible = False
        if not is_text:
            self.spritepath = f'{os.curdir}/interface/{spritename}.png'
            self.sprite = pygame.image.load(self.spritepath)
        else:
            self.spritefont = pygame.font.SysFont(spritename, fontsize)
            self.sprite = self.spritefont.render(text_value, False, fontcolor)

        self.animation = animation
        if self.animation:
            self.sprite = self.animation.sprite

    def routine(self):
        if self.animation:
            self.animation.advance()
            self.sprite = self.animation.sprite


class Counter(Interface):
    def __init__(self, name, x, y, num_val, fontname='ubuntumono', fontsize=24, fontcolor=(0, 0, 0)):
        self.num_val = num_val
        super().__init__(name, x, y, fontname, is_text=True, text_value=str(num_val), fontsize=fontsize, fontcolor=fontcolor)
        self.fontcolor = fontcolor
        self.fontsize = fontsize

    def update_surf(self, newval):
        self.num_val = newval
        self.sprite = self.spritefont.render(str(self.num_val), False, self.fontcolor)


class SplashCounter(Counter):
    def __init__(self, name, x, y, num_val, fontname='ubuntumono', fontsize=24, fontcolor=(0, 0, 0)):
        super().__init__(name, x, y, num_val, fontname=fontname, fontsize=fontsize, fontcolor=fontcolor)
        self.age = 0
        self.destroy = False
        self.visible = True
        self.x_delt = random.randint(-3, 3)
        self.y_delt = random.randint(-3, 3)

    def update_surf(self, newval):
        super().update_surf(newval)

    def routine(self):
        self.update_surf(self.num_val)
        if random.randint(1, 100) >= 80:
            self.y_delt += 1
        self.x += self.x_delt
        self.y += self.y_delt
        self.age += 1
        if self.age >= 100:
            self.destroy = True


class Option(Interface):
    def __init__(self, name, x, y, fontname='ubuntumono', text_val='Text', skill=None,
                 font_col=(0, 0, 0), bg_col=(202, 139, 8), outline_col=(236, 208, 75)):
        super().__init__(name, x, y, fontname, is_text=True, text_value=text_val, fontcolor=font_col)
        sprite_rect = self.sprite.get_rect()
        self.bg_color = bg_col
        self.outline_color = outline_col
        self.rect = pygame.Rect(x-3, y-2, sprite_rect.width+5, sprite_rect.height+2)
        self.clicked = False
        self.skill = skill

    def routine(self):
        self.clicked = False


class Die(Interface):
    def __init__(self, team, x, y, spritename='die'):
        super().__init__(f'{team.name} Die {random.randint(0, 999)}', x, y, f'{spritename}1')
        self.number = 1
        self.die_spritenames = {
            1: f'{spritename}1',
            2: f'{spritename}2',
            3: f'{spritename}3',
            4: f'{spritename}4',
            5: f'{spritename}5',
            6: f'{spritename}6'
        }

    def flip(self):
        self.number = random.randint(1, 6)
        self.sprite = pygame.image.load(f'{os.curdir}/interface/{self.die_spritenames[self.number]}.png')
