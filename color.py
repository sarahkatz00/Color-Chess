#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 20:30:18 2024

@author: sarahkatz
"""

import os
import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        self.pieces = {
            "red":   0,
            "green": 1,
            "blue": 2
        }
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])

    def draw(self, surface, piece_name, coords):
        piece_index = self.pieces[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[piece_index])