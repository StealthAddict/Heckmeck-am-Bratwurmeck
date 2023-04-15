import random
from tkinter import *
from tkinter import ttk
from graphics import *

"""
    TODO: Later, use one of the corner frames to display messages
        like: 'Player 2's turn'.
        Also, label the player boards

    TODO: Player ends their turn by selecting a tile

    TODO: Make subclass specifically for Main Player, which handles changing the buttons
        and selections of dice, etc.
        The main Player subclass can be for the NPCs, and Main Player class overrides some
        functions
"""


def main():
    root = Tk()
   
    root.title('Heckmeck am Bratwurmeck')
    root.resizable(False, False)
    root.config(bg='White')
    board = Board()
    main_player = Player() # Human-controlled player
    frames = create_label_frames(root)
    create_player_labels(frames, main_player, board)
    main_player.assign_board(board)
    # TODO: set up other players w/ objects

    # start_round()

    root.mainloop()
    pass


class Player:
    def __init__(self):
        self.__board = None
        self.__tiles = []  # stores numbered tiles gathered. most recent at top
        self.__rolls_kept = []  # stores numbers selected from rolls
        self.__btns_dice_roll = []
        self.__btns_dice_held = []
        self.__lbl_victory_pts = None
        self.__lbl_dice_pts = None
        self.__btn_top_tile = None
        self.__btn_roll = None

    def set_player_objects(self, po_dictionary):
        self.__btns_dice_roll = po_dictionary['dice roll']
        self.__btns_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self.__btn_top_tile = po_dictionary['tile']
        self.__btn_roll = po_dictionary['button']

    def assign_board(self, board):
        self.__board = board
    
    """
    6's are worms worth 5 pts
    """
    def roll_dice(self):
        num_dice = 8
        rolls = []
        for x in range(num_dice):
            rolls.append(random.randint(1, 6))

        # Change player GUI
        dice_buttons = self.__btns_dice_roll
        for x in range(len(dice_buttons)):
            die = dice_buttons[x]
            roll_number = rolls[x]
            if (rolls[x] == 6):
                roll_number = 'W'
            if die != None:
                die['text'] = roll_number
            
            if die != None:
                if roll_number in self.__rolls_kept:
                    die['state'] = ['disabled']
                else:
                    die['state'] = ['normal']

                if roll_number == 1:
                    die['command'] = lambda: self.select_dice(1)
                elif roll_number == 2:
                    die['command'] = lambda: self.select_dice(2)
                elif roll_number == 3:
                    die['command'] = lambda: self.select_dice(3)
                elif roll_number == 4:
                    die['command'] = lambda: self.select_dice(4)
                elif roll_number == 5:
                    die['command'] = lambda: self.select_dice(5)
                elif roll_number == 'W':
                    die['command'] = lambda: self.select_dice('W')

        if self.__btn_roll is not None:
            self.__btn_roll['state'] = ['disabled']
            # Disable previous choice
            for x in self.__btns_dice_held:
                if x is not None:
                    x['state'] = ['disabled']

        return rolls
    
    def append_tile(self, tile):
        val = tile['val']
        pts = tile['points']
        self.__btn_top_tile['text'] = f'{val} Worms\n{pts} Pts'

    def select_dice(self, number):
        for x in range(len(self.__btns_dice_roll)):            
            die = self.__btns_dice_roll[x]
            
            if die != None and number == die['text']:  
                # Move dice to dice held
                self.__rolls_kept.append(number)
                die.grid(row=3)
                die['command'] = lambda: self.deselect_dice(number)
                self.__btns_dice_held[x] = self.__btns_dice_roll[x]
                self.__btns_dice_roll[x] = None    
            elif die != None:  # Disable unselected dice
                die['state'] = ['disabled']
        
        if self.__btn_roll is not None:  # Enable Roll! button
            self.__btn_roll['state'] = ['normal']

        self.__update_dice_points()

    def deselect_dice(self, number):
        for x in range(len(self.__btns_dice_held)):
            die = self.__btns_dice_held[x]

            if die != None and number == die['text']:
                # Move dice to dice rolled
                self.__rolls_kept.remove(number)
                die.grid(row=2)
                die['command'] = lambda: self.select_dice(number)
                self.__btns_dice_roll[x] = die
                self.__btns_dice_held[x] = None
                
                if self.__btn_roll is not None:  
                    # Disable Roll! button
                    self.__btn_roll['state'] = ['disabled']

        for x in self.__btns_dice_roll: # Re-enable rolled dice
            if x is not None and x['text'] not in self.__rolls_kept: 
                x['state'] = ['normal']
        
        self.__update_dice_points()  

    def __update_dice_points(self):
        # Update dice points  
        d_pts = 0
        for x in self.__rolls_kept:
            d_pts += 5 if x == 'W' else + x
            
        self.__lbl_dice_pts['text'] = f'({d_pts})'

        # Update grill
        self.__board.update_grill_status(d_pts)

    def __update_victory_points(self):
        points = 0
        for x in self.__tiles:
            points += int(x['text'][-5])

        self.__lbl_victory_pts['text'] = points

    def end_turn(self):
        self.__btn_roll['state'] = ['disabled']
        for x in range(len(self.__btns_dice_held)):
            if self.__btns_dice_held[x] != None:
                self.__btns_dice_roll[x] = self.__btns_dice_held[x]
                self.__btns_dice_roll[x].grid(row=2)
                self.__btns_dice_held[x] = None

        for x in range(len(self.__btns_dice_roll)):
            self.__btns_dice_roll[x]['text'] = '/'
            self.__btns_dice_roll[x]['state'] = ['disabled']

        if self.__btn_top_tile not in self.__tiles:
            self.__tiles.append(self.__btn_top_tile)

        self.__rolls_kept = []
        self.__update_dice_points()
        self.__update_victory_points()


class Board:
    def __init__(self):
        self.__board = [] # for graphics
        self.__grill = [] # all available tiles on the board in ascending order.
                          # tiles should be small dictionaries w/ val and status (on grill, w/ player, out of play)
        self.__grill_tiles = [] # button objects of the tiles
        self.__players = [] # list of Player objects playing the game
        
        self.__set_up_grill()

    # Place a tile back onto the board after a player loses it.
    def replace_tile(self, player):
        tile = player.pop_tile()
        tile['status'] = 'grill'
        # TODO: sort tile into correct list index

    def set_grill_tiles(self, grill_tiles):
        self.__grill_tiles = grill_tiles

    def update_grill_status(self, dice_pts):
        for x in range(len(self.__grill_tiles)):
            if self.__grill[x] is not None:
                if self.__grill[x]['val'] <= dice_pts:
                    self.__grill_tiles[x]['state'] = ['normal']
                elif self.__grill[x]['val'] > dice_pts:
                    self.__grill_tiles[x]['state'] = ['disabled']            

    """
    Reset the grill for a new game.
    Replaces all 15 tiles in the grill.
    self.__grill: 'val' - the value needed to acquire the tile
                  'points' - the # of points awarded by the tile
                  'status' - where the tile currently is/availability
    """
    def __set_up_grill(self):
        self.__grill = []
        point_val = 1
        for x in range(21, 37):
            self.__grill.append({'val': x, 'points': point_val,
                                 'status': 'grill'})
            
            # Calculates the correct point values for each tile
            if x % 4 == 0:
                point_val += 1

    def pick_tile(self, player, tile_idx):
        tile = self.__grill[tile_idx - 21]
        player.append_tile(tile)
        player.end_turn()

        self.__grill[tile_idx - 21] = None
        self.__grill_tiles[tile_idx - 21]['state'] = ['disabled']

             

def start_round():
    pass


if __name__ == '__main__':
    main()