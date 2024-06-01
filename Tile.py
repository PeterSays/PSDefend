import pygame
import random

class Tile:
    def __init__(self, row, col, name, mapsize, y_off):
        self.name = name
        self.sprite = pygame.image.load(f'tiles/{name}.png')
        self.rect = self.sprite.get_rect()
        self.clicked = False
        self.row = row
        self.col = col
        self.mapsize = mapsize
        self.x = col*32
        self.y = (row*32) + y_off
        self.y_off = y_off  # from HUD bar
        self.x_offset = 0
        self.y_offset = 0
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.visible = True
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.northwest = None
        self.southwest = None
        self.southeast = None
        self.northeast = None
        self.surrounding = []
        self.temperature = 0

        self.unit_here = None
        self.build_here = None

    def routine(self):
        self.clicked = False

    def initialize(self, tilemap):
        try:
            self.north = tilemap[self.row-1][self.col]
            tilemap[self.row - 1][self.col].south = self
        except IndexError:
            pass

        try:
            self.northwest = tilemap[self.row-1][self.col-1]
            tilemap[self.row - 1][self.col - 1].southeast = self
        except IndexError:
            pass

        try:
            self.northeast = tilemap[self.row-1][self.col+1]
            tilemap[self.row - 1][self.col + 1].southwest = self
        except IndexError:
            pass

        try:
            self.south = tilemap[self.row+1][self.col]
            tilemap[self.row + 1][self.col].north = self
        except IndexError:
            pass

        try:
            self.southwest = tilemap[self.row+1][self.col-1]
            tilemap[self.row + 1][self.col - 1].northeast = self
        except IndexError:
            pass

        try:
            self.southeast = tilemap[self.row+1][self.col+1]
            tilemap[self.row + 1][self.col + 1].northwest = self
        except IndexError:
            pass

        try:
            self.west = tilemap[self.row][self.col-1]
            tilemap[self.row][self.col - 1].east = self
        except IndexError:
            pass

        try:
            self.east = tilemap[self.row][self.col+1]
            tilemap[self.row][self.col + 1].west = self
        except IndexError:
            pass

        self.surrounding = [
            [self.northwest, self.north, self.northeast],
            [self.west, self, self.east],
            [self.southwest, self.south, self.southeast]
        ]

    def surround_list(self):
        sl = []
        for sr in self.surrounding:
            for sc in sr:
                if sc:
                    sl.append(sc)
        return sl

    def nearby_empty(self):
        ne = []
        for sr in self.surrounding:
            for sc in sr:
                if sc and not sc.unit_here:
                    ne.append(sc)
        return ne
