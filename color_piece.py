#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:33:20 2024

@author: sarahkatz
"""

import pygame
import random

class ColorPiece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        
        self.shade_pieces = {
            "WP1":   [5, 255, 0, 0, 127],
            "WP2":   [5, 255, 255, 0, 127],
            "WP3":   [5, 255, 0, 255, 127],
            "WP4":   [5, 0, 255, 255, 127],
            "WP5":   [5, 0, 0, 255, 127],
            "WP6":   [5, 0, 255, 0, 127],
            "WP7":   [5, 255, 0, 0, 127],
            "WP8":   [5, 255, 0, 255, 127],
            "WK1":   [3, 255, 255, 0, 127],
            "WK2":   [3, 0, 255, 0, 127],
            "WB1":   [2, 0, 255, 255, 127],
            "WB2":   [2, 0, 255, 255, 127],
            "WR1":   [4, 255, 0, 0, 127],
            "WR2":   [4, 0, 255, 0, 127],
            "WK":    [0, 255, 0, 0, 127],
            "WQ":    [1, 0, 0, 255, 127],
            "BP1":   [11, 255, 0, 0, 127],
            "BP2":   [11, 255, 0, 255, 127],
            "BP3":   [11, 0, 255, 255, 127],
            "BP4":   [11, 0, 0, 255, 127],
            "BP5":   [11, 255, 0, 0, 127],
            "BP6":   [11, 0, 255, 0, 127],
            "BP7":   [11, 255, 255, 255, 127],
            "BP8":   [11, 255, 255, 0, 127],
            "BK1":   [9, 255, 0, 0, 127],
            "BK2":   [9, 255, 255, 0, 127],
            "BB1":   [8, 255, 0, 0, 127],
            "BB2":   [8, 255, 0, 0, 127],
            "BR1":   [10, 255, 255, 0, 127],
            "BR2":   [10, 255, 0, 255, 127],
            "BK":    [6, 0, 255, 255, 127],
            "BQ":    [7, 0, 255, 0, 127]
        }

        
        # download sprite sheet for sizing
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])
        
        

    def draw(self, surface, piece_name, coords):
        piece_index = self.shade_pieces[piece_name][0]

        # Create a transparent surface
        transparent_surface = pygame.Surface((self.rect.width,self.rect.height), pygame.SRCALPHA)

        # fill the transparant surface with a color and opacity
        shade_dim = (self.shade_pieces[piece_name][1], self.shade_pieces[piece_name][2], self.shade_pieces[piece_name][3], self.shade_pieces[piece_name][4])
        transparent_surface.fill(shade_dim)
        
        # Blit the transparent surface onto the main screen
        surface.blit(transparent_surface, dest=coords, area=self.cells[piece_index])
        