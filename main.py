import random
from tkinter import *
from tkinter import ttk

def main():
    root = Tk()
    root.title('Heckmeck am Bratwurmeck')
    root.resizable(False, False)
    root.config(bg='White')
    board = Board()
    main_player = Player() # Human-controlled player


    root.mainloop()

    pass


class Player:
    def __init__(self):
        self.__tiles = []  # stores numbered tiles gathered. most recent at top
        self.__gathered_dice = []  # stores the dice selected by the player during the round.


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
        num_dice = 8 - len(self.__gathered_dice)
        rolls = []
        for x in range(num_dice):
            rolls.append(random.randint(1, 6))


class Board:
    def __init__(self):
        self.__board = [] # for graphics
        self.__grill = [] # all available tiles on the board in ascending order.
                          # tiles should be small dictionaries w/ val and status (on grill, w/ player, out of play)
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
    def replace_tile(self, tile):
        tile['status'] = 'grill'
        # sort tile into correct list index

        pass

    """
    Reset the grill for a new game.
    Replaces all 15 tiles in the grill.
    self.__grill: 'val' - the value needed to acquire the tile
                  'points' - the # of points awarded by the tile
                  'status' - where the tile currently is
    """
    def __set_up_grill(self):
        self.__grill = []
        point_val = 1
        for x in range(21, 37):
            self.__grill.append({'val': x, 'points': point_val,'status': 'grill'})
            
            # Calculates the correct point values for each tile
            if x % 4 == 0:
                point_val += 1


        


    
    




