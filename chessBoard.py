#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 10:10:28 2024

@author: sarahkatz
"""

import pygame


def build_window():
    # Do logical updates here.
    # ...

    screen.fill("purple")  # Fill the display with a solid color

    # Render the graphics here.
    # ...

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)