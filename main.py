import random
from tkinter import *
from tkinter import ttk
from graphics import *

"""
    TODO: Later, use one of the corner frames to display messages
        like: 'Player 2's turn'.
        Also, label the player boards
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
    
    # TODO: set up other players w/ objects

    start_round()

    root.mainloop()
    pass



class Player:
    def __init__(self):
        self.__tiles = []  # stores numbered tiles gathered. most recent at top
        self.__dice_kept = []  # stores the dice selected by the player during the round.
        self.__player_objects = {}  # labels that keep track of the player's station

    def set_player_objects(self, po_dictionary):
        self.__player_objects = po_dictionary

    """
    Returns the number of points the player has currently acquired. 
    """
    def get_active_points(self):
        points = 0
        for x in self.__tiles:
            points += x['points']

        return points
    
    """
    6's are worms
    """
    def roll_dice(self):
        num_dice = 8
        rolls = []
        for x in range(num_dice):
            rolls.append(random.randint(1, 6))

        # print(rolls)

        # Change player GUI
        dice_buttons = self.__player_objects['dice roll']
        for x in range(len(dice_buttons)):
            die = dice_buttons[x]
            if (rolls[x] == 6) and die != None:
                die['text'] = 'W'
            elif die != None:
                die['text'] = rolls[x]
            
            if die != None:
                die['state'] = ['normal']
                if rolls[x] == 1:
                    die['command'] = lambda: self.select_dice(1)
                elif rolls[x] == 2:
                    die['command'] = lambda: self.select_dice(2)
                elif rolls[x] == 3:
                    die['command'] = lambda: self.select_dice(3)
                elif rolls[x] == 4:
                    die['command'] = lambda: self.select_dice(4)
                elif rolls[x] == 5:
                    die['command'] = lambda: self.select_dice(5)
                elif rolls[x] == 6:
                    die['command'] = lambda: self.select_dice('W')

        return rolls

    def pop_tile(self):
        return self.__tiles.pop()
    
    def select_dice(self, number):
        for x in range(len(self.__player_objects['dice roll'])):
            die = self.__player_objects['dice roll'][x]
            if die != None and number == die['text']:
                die.grid(row=3)
                die['command'] = lambda: self.deselect_dice(number)
                self.__player_objects['dice held'][x] = self.__player_objects['dice roll'][x]
                self.__player_objects['dice roll'][x] = None
    
    def deselect_dice(self, number):
        for x in range(len(self.__player_objects['dice held'])):
            die = self.__player_objects['dice held'][x]
            if die != None and number == die['text']:
                die.grid(row=2)
                die['command'] = lambda: self.select_dice(number)
                self.__player_objects['dice roll'][x] = die
                self.__player_objects['dice held'][x] = None
                    

class Board:
    def __init__(self):
        self.__board = [] # for graphics
        self.__grill = [] # all available tiles on the board in ascending order.
                          # tiles should be small dictionaries w/ val and status (on grill, w/ player, out of play)
        self.__grill_tiles = [] # button objects of the tiles
        self.__players = [] # list of Player objects playing the game
        
        self.__set_up_grill()

    # Remove a tile from the board, whether it moves to a player or is out of play
    def remove_tile(self, tile):
        if tile in self.__grill:
            self.__grill.remove(tile)
        else:
            print("ERROR: Tile not in grill.")
            print("TILE: ", tile)

    # Place a tile back onto the board after a player loses it.
    def replace_tile(self, player):
        tile = player.pop_tile()
        tile['status'] = 'grill'
        # TODO: sort tile into correct list index

    def set_grill_tiles(self, grill_tiles):
        self.__grill_tiles = grill_tiles

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
            self.__grill.append({'val': x, 'points': point_val,'status': 'grill'})
            
            # Calculates the correct point values for each tile
            if x % 4 == 0:
                point_val += 1

def start_round():
    pass

if __name__ == '__main__':
    main()