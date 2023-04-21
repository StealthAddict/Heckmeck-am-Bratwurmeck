import random
import time
from tkinter import *
# from main import Board

class MainPlayer():

    def __init__(self):
        self.__board = None
        self.__tiles = []  # stores numbered tiles gathered. most recent at top
        self.__rolls_kept = []  # stores numbers selected from rolls
        self.__btns_dice_roll = []
        self.__btns_dice_held = []
        self.__lbl_victory_pts = None
        self.__lbl_dice_pts = None
        self._btn_top_tile = None
        self.__btn_roll = None
        self.txt_notif = StringVar()

    def set_player_objects(self, po_dictionary, board):
        self.__btns_dice_roll = po_dictionary['dice roll']
        self.__btns_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self._btn_top_tile = po_dictionary['tile']
        self.__btn_roll = po_dictionary['button']
        self.__board = board
    
    def roll_dice(self):
        """For use by roll! button. Randomly rolls dice between 1-6 for 
        the main player to select from. Dice that roll a 6 are indicated
        by a 'W' for worm.
        """
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

        # Check if the player can choose from the roll
        invalid_dice, total_dice = self.__get_ti_dice_cnt()
        if invalid_dice == total_dice and total_dice != 0:  
            self.__turn_bust("No selectable dice.")

        return rolls
    
    def __turn_bust(self, bust_str):
        """A bust causes the top tile of the player's
        tile stack to be returned to the grill. If no tiles
        remain, the largest value grill tile is now out of play.
        """
        if len(self.__tiles) < 1:
            self.__board.remove_tile_from_play()
        else:
            removed_tile = self.__tiles.pop(-1)
            removed_tile['status'] = 'grill'
            removed_tile['object']['state'] = ['disabled']
            if len(self.__tiles) > 0:
                self._btn_top_tile['text'] = self.__tiles[-1]['object']['text']

        self.txt_notif.set(f'Busted!\n{bust_str}')
        self.end_turn() 

    def update_top_tile(self, tile):
        """ Updates the player's tile button to be the tile parameter.
        Adds the tile onto the player's collection of tiles.
        """
        self._btn_top_tile['text'] = tile['object']['text']
        if tile not in self.__tiles:
            self.__tiles.append(tile)
        else:
            self.__tiles.remove(tile)

    def __get_ti_dice_cnt(self):
        """ Returns the total dice left in the roll and the 
        invalid dice in the roll. Invalid dice are dice the 
        player cannot select.
        """
        invalid_dice = 0
        total_dice = 0
        for x in self.__btns_dice_roll:  # Check dice
            if x is not None:
                total_dice += 1
                if x['state'] == 'disabled':
                    invalid_dice += 1
        return invalid_dice, total_dice

    def select_dice(self, number):
        """ Moves all dice of one number from the dice rolled row to the
        dice kept row.
        """
        for x in range(len(self.__btns_dice_roll)):            
            die = self.__btns_dice_roll[x]
            
            if die != None and number == die['text']:  
                # Move dice to dice held
                self.__rolls_kept.append(number)
                die.grid(row=4)
                die['command'] = lambda: self.deselect_dice(number)
                self.__btns_dice_held[x] = self.__btns_dice_roll[x]
                self.__btns_dice_roll[x] = None    
            elif die != None:  # Disable unselected dice
                die['state'] = ['disabled']
        
        if self.__btn_roll is not None:  # Enable Roll! button
            self.__btn_roll['state'] = ['normal']

        d_pts = self.__update_dice_points()

        # Check if any tiles are selectable after there are no
        # more dice to roll.
        invalid_dice, total_dice = self.__get_ti_dice_cnt()
        if total_dice == 0:
            available_tile = False
            grill = self.__board.get_grill()
            for x in grill:
                if x['val'] > d_pts:
                    self.__turn_bust("Can't purchase any tiles.")
                    break
                elif x['object']['state'] == 'normal':
                    available_tile = True
                    break
            
            if not available_tile:
                self.__turn_bust("Can't purchase any tiles.")

            elif not self.has_worms():
                self.__turn_bust("You have no worms.")

    def deselect_dice(self, number):
        """ Moves all dice of one number from the dice kept row to the
        dice rolled row.
        """
        for x in range(len(self.__btns_dice_held)):
            die = self.__btns_dice_held[x]

            if die != None and number == die['text']:
                # Move dice to dice rolled
                self.__rolls_kept.remove(number)
                die.grid(row=3)
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
        """ Update dice points label and
        update grill status based on dice points.
            Returns dice point amount.
        """
        d_pts = 0
        for x in self.__rolls_kept:
            d_pts += 5 if x == 'W' else + x
            
        self.__lbl_dice_pts['text'] = f'({d_pts})'
        self.__board.update_grill_status(d_pts)

        return d_pts

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
                self.__btns_dice_roll[x].grid(row=3)
                self.__btns_dice_held[x] = None

        for x in range(len(self.__btns_dice_roll)):
            self.__btns_dice_roll[x]['text'] = '/'
            self.__btns_dice_roll[x]['state'] = ['disabled']

        self.__rolls_kept = []
        self.__update_dice_points()
        self.__update_victory_points()
        self.__board.activate_next_player()

    def has_worms(self):
        for x in self.__btns_dice_held:
            if x is not None and x['text'] == 'W':
                return True
            
        return False
    
    def activate_play(self):
        # Normalize roll! button
        self.__btn_roll['state'] = ['normal']

        self.txt_notif.set('')
        print("main player's turn")


class Player():
    def __init__(self):
        self.__board = None
        self.__tiles = []  # stores numbered tiles gathered. most recent at top
        self.__rolls_kept = []  # stores numbers selected from rolls
        self.__lbls_dice_roll = []
        self.__lbls_dice_held = []
        self.__lbl_victory_pts = None
        self.__lbl_dice_pts = None
        self._btn_top_tile = None
        self.__btn_roll = None
        self.txt_notif = StringVar()

    def set_player_objects(self, po_dictionary, board):
        self.__lbls_dice_roll = po_dictionary['dice roll']
        self.__lbls_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self._btn_top_tile = po_dictionary['tile']
        self.__board = board


class CasualPlayer(Player):

    def __init__(self):
        parent = super(CasualPlayer, self)
        parent.__init__()
        self.__parent = parent

    
    def activate_play(self):
        # Perform casual player's actions

        # roll dice
        # choose dice
        # check if tiles are available
        # repeat until desired points reached
        # select a tile
        # end turn

        self.txt_notif.set('')
        print("casual player's turn")