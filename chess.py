#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:38:47 2024

@author: sarahkatz
"""

import pygame
from pygame.locals import *
import random

from chess_piece import ChessPiece
from color_piece import ColorPiece
from utils import Utils

import time

class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # display surface
        self.screen = screen
        # create an object of class to show chess pieces on the board
        self.chess_pieces = ChessPiece(pieces_src, cols=6, rows=2)
        # create an object of class to show color pieces on the board
        self.color_pieces = ColorPiece(pieces_src, cols=6, rows=2)
        # store coordinates of the chess board squares
        self.board_locations = square_coords
        # length of the side of a chess board square
        self.square_length = square_length
        # dictionary to keeping track of player turn
        self.turn = {"black": 0,
                     "white": 0}

        # list containing possible moves for the selected piece
        self.moves = []
        #
        self.utils = Utils()

        # mapping of piece names to index of list containing piece coordinates on spritesheet
        self.game_pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }
        

        # list containing captured pieces
        self.captured = []
        #
        self.winner = ""

        self.reset()
    
    def reset(self):
        # clear moves lists
        self.moves = []

        # randomize player turn
        x = random.randint(0, 1)
        if(x == 1):
            self.turn["black"] = 1
        elif(x == 0):
            self.turn["white"] = 1

        # two dimensonal dictionary containing details about each board location
        # storage format is [piece_name, currently_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a>0:
                # [piece name, shade name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", "", False, [x,y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # reset the board - pieces
        for i in range(97, 105):
            x = 8
            while x>0:
                if(x==8):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif(x==7):
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif(x==2):
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif(x==1):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1
                
        # reset the board - color shading
        for i in range(97, 105):
            x = 8
            while x>0:
                if(x==8):
                    if(chr(i)=='a'):
                        self.piece_location[chr(i)][x][1] = "BR1"
                    elif(chr(i)=='h'):
                        self.piece_location[chr(i)][x][1] = "BR2"
                    elif(chr(i)=='b'):
                        self.piece_location[chr(i)][x][1] = "BK1"
                    elif(chr(i)=='g'):
                        self.piece_location[chr(i)][x][1] = "BK2"
                    elif(chr(i)=='c'):
                        self.piece_location[chr(i)][x][1] = "BB1"
                    elif(chr(i)=='f'):
                        self.piece_location[chr(i)][x][1] = "BB2"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][1] = "BQ"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][1] = "BK"
                elif(x==7):
                    if(chr(i)=='a'):
                        self.piece_location[chr(i)][x][1] = "BP1"
                    elif(chr(i)=='b'):
                        self.piece_location[chr(i)][x][1] = "BP2"
                    elif(chr(i)=='c'):
                        self.piece_location[chr(i)][x][1] = "BP3"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][1] = "BP4"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][1] = "BP5"
                    elif(chr(i)=='f'):
                        self.piece_location[chr(i)][x][1] = "BP6"
                    elif(chr(i)=='g'):
                        self.piece_location[chr(i)][x][1] = "BP7"
                    elif(chr(i)=='h'):
                        self.piece_location[chr(i)][x][1] = "BP8"
                elif(x==2):
                    if(chr(i)=='a'):
                        self.piece_location[chr(i)][x][1] = "WP1"
                    elif(chr(i)=='b'):
                        self.piece_location[chr(i)][x][1] = "WP2"
                    elif(chr(i)=='c'):
                        self.piece_location[chr(i)][x][1] = "WP3"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][1] = "WP4"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][1] = "WP5"
                    elif(chr(i)=='f'):
                        self.piece_location[chr(i)][x][1] = "WP6"
                    elif(chr(i)=='g'):
                        self.piece_location[chr(i)][x][1] = "WP7"
                    elif(chr(i)=='h'):
                        self.piece_location[chr(i)][x][1] = "WP8"
                elif(x==1):
                    if(chr(i)=='a'):
                        self.piece_location[chr(i)][x][1] = "WR1"
                    elif(chr(i)=='h'):
                        self.piece_location[chr(i)][x][1] = "WR2"
                    elif(chr(i)=='b'):
                        self.piece_location[chr(i)][x][1] = "WK1"
                    elif(chr(i)=='g'):
                        self.piece_location[chr(i)][x][1] = "WK2"
                    elif(chr(i)=='c'):
                        self.piece_location[chr(i)][x][1] = "WB1"
                    elif(chr(i)=='f'):
                        self.piece_location[chr(i)][x][1] = "WB2"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][1] = "WQ"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][1] = "WK"
                x = x - 1

    # 
    def play_turn(self):
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        if self.turn["black"]:
            turn_text = small_font.render("Turn: Black", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Turn: White", True, white_color)
        
        # show welcome text
        self.screen.blit(turn_text, 
                      ((self.screen.get_width() - turn_text.get_width()) // 2,
                      10))
        
        # let player with black piece play
        if(self.turn["black"]):
            self.move_piece("black")
        # let player with white piece play
        elif(self.turn["white"]):
            self.move_piece("white")

    # method to draw pieces on the chess board
    def draw_pieces(self):
        transparent_gray = (0,0,0,150)

        # create a transparent surface
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_gray)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_gray)

        # loop to change background color of selected piece
        for val in self.piece_location.values():
            for value in val.values() :
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[3]

                # change background color of piece if it is selected
                if value[2] and len(value[0]) > 5:
                    # if the piece selected is a black piece
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # if the piece selected is a white piece
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])
     

        # draw all chess pieces
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # name of the shade in the current location
                shade_name = value[1]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[3]
                # check if there is a piece at the square
                if(len(value[0]) > 1):
                    self.chess_pieces.draw(self.screen, piece_name, 
                                            self.board_locations[piece_coord_x][piece_coord_y])
                    
                    self.color_pieces.draw(self.screen, shade_name, 
                                            self.board_locations[piece_coord_x][piece_coord_y])
                                        
    # method to find the possible moves of the selected piece
    def possible_moves(self, piece_name, piece_coord):
        # list to store possible moves of the selected piece
        positions = []
        # find the possible locations to put a piece
        if len(piece_name) > 0:
            # get x, y coordinate
            x_coord, y_coord = piece_coord
            # calculate moves for bishop
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
            
            # calculate moves for pawn
            elif piece_name[6:] == "pawn":
                # convert list index to dictionary key
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # calculate moves for white pawn
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # get row in front of black pawn
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                
                        # pawns cannot move when blocked by another another pawn
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord+1])
                            # black pawns can move two positions ahead for first move
                            if y_coord < 2:
                                positions.append([x_coord, y_coord+2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1
                            
                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                        # diagonal to the right
                        if x_coord + 1 < 8  and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                # calculate moves for white pawn
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # get row in front of black pawn
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord-1])
                            # black pawns can move two positions ahead for first move
                            if y_coord > 5:
                                positions.append([x_coord, y_coord-2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1
                            
                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])

                            
                        # diagonal to the right
                        if x_coord + 1 < 8  and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])


            # calculate moves for rook
            elif piece_name[6:] == "rook":
                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # calculate moves for knight
            elif piece_name[6:] == "knight":
                # left positions
                if(x_coord - 2) >= 0:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-2, y_coord+1])
                # top positions
                if(y_coord - 2) >= 0:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord-2])
                # right positions
                if(x_coord + 2) < 8:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+2, y_coord+1])
                # bottom positions
                if(y_coord + 2) < 8:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord+2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+2])

            # calculate movs for king
            elif piece_name[6:] == "king":
                if(y_coord - 1) >= 0:
                    # top spot
                    positions.append([x_coord, y_coord-1])

                if(y_coord + 1) < 8:
                    # bottom spot
                    positions.append([x_coord, y_coord+1])

                if(x_coord - 1) >= 0:
                    # left spot
                    positions.append([x_coord-1, y_coord])
                    # top left spot
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-1])
                    # bottom left spot
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-1, y_coord+1])
                    
                if(x_coord + 1) < 8:
                    # right spot
                    positions.append([x_coord+1, y_coord])
                    # top right spot
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+1, y_coord-1])
                    # bottom right spot
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+1])
                
            # calculate movs for queen
            elif piece_name[6:] == "queen":
                # find diagonal positions
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # list of positions to be removed
            to_remove = []

            # remove positions that overlap other pieces of the current player
            for pos in positions:
                x, y = pos

                # convert list index to dictionary key
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # find the pieces to remove
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if(des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # remove position from positions list
            for i in to_remove:
                positions.remove(i)

        # return list containing possible moves for the selected piece
        return positions


    def move_piece(self, turn):
        # get the coordinates of the square selected on the board
        square = self.get_selected_square()

        # if a square was selected
        if square:
            # get name of piece on the selected square
            piece_name = square[0]
            # get name of shade on the selected square
            shade_name = square[1]
            # color of piece on the selected square
            piece_color = piece_name[:5]
            # board column character
            columnChar = square[2]
            # board row number
            rowNo = square[3]

            # get x, y coordinates
            x, y = self.piece_location[columnChar][rowNo][3]

            # if there's a piece on the selected square
            if(len(piece_name) > 0) and (piece_color == turn):
                # find possible moves for the piece
                self.moves = self.possible_moves(piece_name, [x,y])

            # checkmate mechanism
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if(p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x,y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x,y])

            # only the player with the turn gets to play
            if(piece_color == turn):
                # change selection flag from all other pieces
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][2] = False
                    
                # change selection flag of the selected piece
                self.piece_location[columnChar][rowNo][2] = True
                
            # check board for color game win
            self.check_color_board()
                    
            
    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1], 
                            self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    #reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values() :
                                            # [piece name, currently selected, board coordinates]
                                            if not value[2]:
                                                value[2] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the piece
                                    piece_name = self.piece_location[columnChar][rowNo][0]
                                    # get the name of the shade
                                    shade_name = self.piece_location[columnChar][rowNo][1]
                                    
                                    return [piece_name, shade_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None


    def check_color_board(self):
        # check if overall opacity for the board is at 75%?
        # sum the total opacity for each piece
        # then calc avg
        # if threshold reached, then declare the game won
        # UPDATE HERE!!!
        sum_shade = 0
        
        for col in range(97, 105):
            for row in range(1, 9):
                colChar = chr(col)
                shade_name = self.piece_location[colChar][row][1]
                if (len(shade_name)>0):
                    shade_value = self.color_pieces.shade_pieces[shade_name][4]
                    sum_shade += shade_value
        
        # 32 pieces in the game (should this be updated if pieces are captured?)
        avg_shade = sum_shade/32     
        print('avg shade: {}'.format(avg_shade))
        # shade starting at 127 (50% opacity); winning = 191 (75% opacity)
        if (avg_shade > 191):
            self.winner = "Color"
            print("Game won")
                

    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]
        
        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)


    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[2]:
                    # unselect the source piece
                    self.piece_location[k][key][2] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]
                    # move the source piece to the destination piece
                    self.piece_location[desColChar][desRowNo][0] = piece_name
                    # get the name of the source shade
                    shade_name = self.piece_location[k][key][1]
                    # move the source shade to the destination shade
                    self.piece_location[desColChar][desRowNo][1] = shade_name
                    
                    src_name = self.piece_location[k][key][0]
                    # remove source piece from its current position
                    self.piece_location[k][key][0] = ""
                    self.piece_location[k][key][1] = ""

                    # change turn
                    if(self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif("white"):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(src_name,  src_location, des_location))
                    
                    
                    # get shade and color of selected piece
                    selected_shade = self.color_pieces.shade_pieces[shade_name][4]
                    selected_R_color = self.color_pieces.shade_pieces[shade_name][1]
                    selected_G_color = self.color_pieces.shade_pieces[shade_name][2]
                    selected_B_color = self.color_pieces.shade_pieces[shade_name][3]                    
                    # get current color of "moved piece"
                    selected_color = (selected_R_color, selected_G_color, selected_B_color)

                    
                    # check each piece surrounding the moved piece
                    surrounding_spaces = [(1,-1), (1,0), (1,1), (0,-1), (0,1), (-1,-1), (-1,0), (-1,1)]
                    for space in surrounding_spaces:
                        # calculate "check space"
                        row = desRowNo+space[0]
                        col_value = ord(desColChar)+space[1]
                        col = chr(col_value)
                        
                        # verify "check space" is on the board
                        if((row>0) & (row<9) & (col_value>97) & (col_value<105)):
                            if(len(self.piece_location[col][row][1])>0):
                                # get color of "check space"
                                check_shade_name = self.piece_location[col][row][1]
                                
                                check_shade = self.color_pieces.shade_pieces[check_shade_name][4]
                                check_R_color = self.color_pieces.shade_pieces[check_shade_name][1]
                                check_G_color = self.color_pieces.shade_pieces[check_shade_name][2]
                                check_B_color = self.color_pieces.shade_pieces[check_shade_name][3]
                                check_color = (check_R_color, check_G_color, check_B_color)
                                
                                if(selected_color == check_color):
                                    print('{} has a color match with {}'.format(shade_name, check_shade_name))
                                    # update selected shade (if not at full opacity)
                                    if(selected_shade < 224):
                                        self.color_pieces.shade_pieces[shade_name][4] = selected_shade + 32
                                    # updatechecked shade
                                    if(check_shade < 224):
                                        self.color_pieces.shade_pieces[check_shade_name][4] = check_shade + 32
                       

    # helper function to find diagonal moves
    def diagonal_moves(self, positions, piece_name, piece_coord):
        # reset x and y coordinate values
        x, y = piece_coord
        # find top left diagonal spots
        while(True):
            x = x - 1
            y = y - 1
            if(x < 0 or y < 0):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom right diagonal spots
        while(True):
            x = x + 1
            y = y + 1
            if(x > 7 or y > 7):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom left diagonal spots
        while(True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find top right diagonal spots
        while(True):
            x = x + 1
            y = y - 1
            if(x > 7 or y < 0):
                break
            else:
                positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions
    

    # helper function to find horizontal and vertical moves
    def linear_moves(self, positions, piece_name, piece_coord):
        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the left
        while(x > 0):
            x = x - 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
                    

        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the right
        while(x < 7):
            x = x + 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break    

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves upwards
        while(y > 0):
            y = y - 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves downwards
        while(y < 7):
            y = y + 1
            positions.append([x,y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break


        return positions
    
    