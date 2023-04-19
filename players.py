import random
import time
from tkinter import *

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

    def _get_player_objects(self):
        """ For use of child player classes to access needed variables.
        """
        return {'btn_dice_roll': self.__btns_dice_roll,
                'btn_roll': self.__btn_roll}

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


class MainPlayer(Player):

    def __init__(self):
        parent = super(MainPlayer, self)
        parent.__init__()
        self.__parent = parent
    
    def activate_play(self):
        # Normalize roll! button
        po_dict = self.__parent._get_player_objects()
        po_dict['btn_roll']['state'] = ['normal']

        print("main player's turn")

class CasualPlayer(Player):

    def __init__(self):
        super(CasualPlayer, self).__init__()
    
    def activate_play(self):
        # Perform casual player's actions

        print("casual player's turn")