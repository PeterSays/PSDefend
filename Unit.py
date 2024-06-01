import random

import pygame
import os
from Tile import Tile
from Material import Material
from Animated import Animated
from random import randint

class Unit:
    def __init__(self, name, spritename, spawntile: Tile, stats_dict, skill_list=None, material=None, is_base=False, is_build=False):
        self.name = name
        self.stats_dict = stats_dict

        self.max_hp = self.stats_dict['hp']
        self.hp = self.stats_dict['hp']
        self.max_mp = self.stats_dict['mp']
        self.mp = self.stats_dict['mp']
        self.strength = self.stats_dict['strength']
        self.toughness = self.stats_dict['toughness']
        self.agility = self.stats_dict['agility']
        self.intelligence = self.stats_dict['intelligence']

        self.skill_list = skill_list
        if not skill_list:
            self.skill_list = []

        self.is_base = is_base
        self.is_build = is_build

        self.team = None

        self.on_col = spawntile.col
        self.on_row = spawntile.row
        self.on_tile = spawntile
        spawntile.unit_here = self

        self.x = self.on_col*32
        self.y = (self.on_row*32) + spawntile.y_off
        self.dest_x = self.x
        self.dest_y = self.y
        self.speed = 1
        self.movement_cost = 1

        if self.is_base:
            self.folderpath = f'{os.curdir}/units/{spritename}'
            folder_list = os.listdir(self.folderpath)
            animation_seq = []
            for filename in folder_list:
                frame_img = pygame.image.load(f'{self.folderpath}/{filename}')
                animation_seq.append(frame_img)
            self.animation = Animated(f'{spritename} Idle', animation_seq, frametime=5)
        elif self.is_build:
            self.folderpath = f'{os.curdir}/units/builds/'
            frame_img = pygame.image.load(f'{self.folderpath}/{spritename}.png')
            animation_seq = [frame_img]
            self.animation = Animated(f'{spritename} Idle', animation_seq)
        else:
            self.folderpath = f'{os.curdir}/units/'
            spritepath = f'{self.folderpath}/{spritename}.png'
            frame_img = pygame.image.load(spritepath)
            animation_seq = [frame_img]
            self.animation = Animated(f'{spritename} Idle', animation_seq)

        # self.ani_frametime = 10
        # self.ani_timer = self.ani_frametime
        # self.ani_index = 0

        self.sprite = self.animation.sprite
        sprite_rect = self.sprite.get_rect()
        self.y_offset = 0
        if sprite_rect.height > 32:
            self.y_offset = (sprite_rect.height - 32) * -1
        elif sprite_rect.height < 32:
            self.y_offset = sprite_rect.height - 32
        self.x_offset = 0
        self.rect = pygame.Rect(self.x+self.x_offset, self.y+self.y_offset, 32, 32)
        self.clicked = False
        self.visible = True
        self.sprite_changed = False
        self.center_x = round(self.sprite.get_width()/2)
        self.center_y = round(self.sprite.get_height()/2)
        self.going = False

        self.material = material
        if not self.material:
            self.material = Material(f'{name} Flesh', 'demon', temp_conduct=0.5, heat_dam=80, cold_dam=-80,
                                     color_a=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                     color_b=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def change_pos(self, x_mov=0, y_mov=0):
        self.x += x_mov
        self.y += y_mov

    def open_adjacents(self):  # for movement
        surround = [self.on_tile.north, self.on_tile.northeast, self.on_tile.east, self.on_tile.southeast,
                    self.on_tile.south, self.on_tile.southwest, self.on_tile.west, self.on_tile.northwest]
        go_able = []
        for t in surround:
            if not t.unit_here:
                go_able.append(t)
        return go_able

    def in_range(self, used_skill):
        if used_skill.targ_type == 'adjacent':
            surround = [self.on_tile.north, self.on_tile.northeast, self.on_tile.east, self.on_tile.southeast,
                        self.on_tile.south, self.on_tile.southwest, self.on_tile.west, self.on_tile.northwest]
            go_able = []
            for t in surround:
                if t.unit_here:
                    go_able.append(t.unit_here)
            return go_able

    def routine(self):
        if self.animation:
            self.animation.advance()
            self.sprite = self.animation.sprite

        # self.sprite_changed = False
        # self.clicked = False

        # self.ani_timer -= 1
        # if self.ani_timer <= 0:
        #     self.sprite_changed = True
        #     self.ani_timer = self.ani_frametime
        #     self.ani_index += 1
        #     if self.ani_index > len(self.animation) - 1:
        #         self.ani_index = 0

        # if self.sprite_changed and self.spritepath != self.animation[self.ani_index]:
        #    self.spritepath = self.animation[self.ani_index]
        #     self.sprite = pygame.image.load(self.spritepath)

        if self.dest_x != self.x and self.speed < abs(self.dest_x - self.x):
            if self.dest_x > self.x:
                self.change_pos(x_mov=self.speed)
            else:
                self.change_pos(x_mov=self.speed * -1)
        elif self.dest_x != self.x:
            self.x = self.dest_x

        if self.dest_y != self.y and self.speed < abs(self.dest_y - self.y):
            if self.dest_y > self.y:
                self.change_pos(y_mov=self.speed)
            else:
                self.change_pos(y_mov=self.speed * -1)
        elif self.dest_y != self.y:
            self.y = self.dest_y

        self.rect.x = self.x
        self.rect.y = self.y


class Build(Unit):
    def __init__(self, buildname, spritename, spawntile, stats_dict, material):
        super().__init__(buildname, spritename, spawntile, stats_dict, material, is_build=True)
        self.movement_cost = 0
