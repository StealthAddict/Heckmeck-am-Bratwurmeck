import random
from tkinter import *
from tkinter import ttk
from graphics import *
import time 

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
    players = [main_player, Player(), Player(), Player()]
    frames = create_label_frames(root)
    create_player_labels(frames, players, board)

    board.assign_players(players)
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

    def set_player_objects(self, po_dictionary, board):
        self.__btns_dice_roll = po_dictionary['dice roll']
        self.__btns_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self.__btn_top_tile = po_dictionary['tile']
        self.__btn_roll = po_dictionary['button']
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

                match roll_number:
                    case 1:
                        die['command'] = lambda: self.select_dice(1)
                    case 2:
                        die['command'] = lambda: self.select_dice(2)
                    case 3:
                        die['command'] = lambda: self.select_dice(3)
                    case 4:
                        die['command'] = lambda: self.select_dice(4)
                    case 5:
                        die['command'] = lambda: self.select_dice(5)
                    case 'W':
                        die['command'] = lambda: self.select_dice('W')

        if self.__btn_roll is not None:
            self.__btn_roll['state'] = ['disabled']
            # Disable previous choice
            for x in self.__btns_dice_held:
                if x is not None:
                    x['state'] = ['disabled']

        # Check for a bust
        invalid_dice = 0
        total_dice = 0
        for x in self.__btns_dice_roll:
            if x is not None:
                total_dice += 1
                if x['state'] == 'disabled':
                    invalid_dice += 1
        if invalid_dice == total_dice and total_dice != 0:
            # should have a little notif in the player station instead to show 'busted'
            self.__board.set_notification("Busted!")
            self.end_turn()

        # or if no tiles are 'normal' and total_dice == 0

        return rolls
    
    def update_top_tile(self, tile):
        self.__btn_top_tile['text'] = tile['object']['text']
        if tile not in self.__tiles:
            self.__tiles.append(tile)
        else:
            self.__tiles.remove(tile)

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
            points += x['points']

        self.__lbl_victory_pts['text'] = points

    def end_turn(self):
        # Reset dice
        self.__btn_roll['state'] = ['disabled']
        for x in range(len(self.__btns_dice_held)):
            if self.__btns_dice_held[x] != None:
                self.__btns_dice_roll[x] = self.__btns_dice_held[x]
                self.__btns_dice_roll[x].grid(row=2)
                self.__btns_dice_held[x] = None

        for x in range(len(self.__btns_dice_roll)):
            self.__btns_dice_roll[x]['text'] = '/'
            self.__btns_dice_roll[x]['state'] = ['disabled']

        self.__rolls_kept = []
        self.__update_dice_points()
        self.__update_victory_points()
        self.__board.activate_next_player()

    def activate_play(self):
       
        """ run AI or for main, activate dice buttons
            Could create a subclass for every player/AI type
            and this one just immediately ends turn as its the player
            thats not assigned to play
        """
        print("this player's turn!")

class Board:
    def __init__(self):
        self.__grill = [] # all available tiles on the board in ascending order.
        self.players = [] # list of Player objects playing the game
        self.__next_player = 0  # index of next player
        self.__game_over = False
        self.txt_notif = None
        

    # Place a tile back onto the board after a player loses it.
    def replace_tile(self, player):
        tile = player.pop_tile()
        tile['status'] = 'grill'
        # TODO: sort tile into correct list index

    def update_grill_status(self, dice_pts):
        for x in range(len(self.__grill)):
            if self.__grill[x] is not None and self.__grill[x]['status'] == 'grill':
                if self.__grill[x]['val'] <= dice_pts:
                    self.__grill[x]['object']['state'] = ['normal']
                elif self.__grill[x]['val'] > dice_pts:
                    self.__grill[x]['object']['state'] = ['disabled']    
            elif self.__grill[x] is not None and self.__grill[x]['val'] == dice_pts:
                self.__grill[x]['object']['state'] = ['normal']

    """
    Reset the grill for a new game.
    Replaces all 15 tiles in the grill.
    self.__grill: 'val' - the value needed to acquire the tile
                  'points' - the # of points awarded by the tile
                  'status' - where the tile currently is/availability
    """
    def set_up_grill(self, grill_tiles):
        self.__grill = []
        point_val = 1
        for x in range(21, 37):
            self.__grill.append({'val': x, 'points': point_val,
                                 'status': 'grill', 
                                 'object': grill_tiles[x - 21]})
            
            # Calculates the correct point values for each tile
            if x % 4 == 0:
                point_val += 1

    def set_notification(self, new_string):
        self.txt_notif.set(new_string)        

    def pick_tile(self, player, tile_idx):
        tile = self.__grill[tile_idx - 21]
        player.update_top_tile(tile)
        player.end_turn()

        self.__grill[tile_idx - 21]['status'] = player
        self.__grill[tile_idx - 21]['object']['state'] = ['disabled']

    def assign_players(self, player_list):
        self.players = player_list

    def activate_next_player(self):
        if not self.__game_over:
            self.players[self.__next_player].activate_play()
            self.__next_player = 0 if self.__next_player == 3 else + 1
            self.set_notification(f'Player {self.__next_player + 1}\'s turn!')
        else:
            print('GAME OVER')


if __name__ == '__main__':
    main()