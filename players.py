import random
from tkinter import *
from main import tksleep


class MainPlayer:

    def __init__(self):
        self.__board = None
        self.__tiles = []  # stores tiles gathered. most recent at top
        self.__rolls_kept = []  # stores numbers selected from rolls
        self.__btns_dice_roll = []
        self.__btns_dice_held = []
        self.__lbl_victory_pts = None
        self.__lbl_dice_pts = None
        self.btn_top_tile = None
        self.__btn_roll = None
        self.txt_notif = StringVar()

    def set_player_objects(self, po_dictionary, board):
        self.__btns_dice_roll = po_dictionary['dice roll']
        self.__btns_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self.btn_top_tile = po_dictionary['tile']
        self.__btn_roll = po_dictionary['button']
        self.__board = board

    def activate_play(self):
        # Normalize roll! button
        self.__btn_roll['state'] = ['normal']
        self.txt_notif.set('')

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
            if rolls[x] == 6:
                roll_number = 'W'
            if die is not None:
                die['text'] = roll_number

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

        # Check if the player can choose from the roll
        invalid_dice, total_dice = self.__get_ti_dice_cnt()
        if invalid_dice == total_dice and total_dice != 0:
            self.__turn_bust("No selectable dice.")

        return rolls

    def select_dice(self, number):
        """ Moves all dice of one number from the dice rolled row to the
        dice kept row.
        """
        for x in range(len(self.__btns_dice_roll)):
            die = self.__btns_dice_roll[x]

            if die is not None and number == die['text']:
                # Move dice to dice held
                self.__rolls_kept.append(number)
                die.grid(row=4)
                die['command'] = lambda: self.deselect_dice(number)
                self.__btns_dice_held[x] = self.__btns_dice_roll[x]
                self.__btns_dice_roll[x] = None
            elif die is not None:  # Disable unselected dice
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
                if x['object']['state'] == 'normal':
                    available_tile = True
                    break
                elif x['val'] > d_pts:
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

            if die is not None and number == die['text']:
                # Move dice to dice rolled
                self.__rolls_kept.remove(number)
                die.grid(row=3)
                die['command'] = lambda: self.select_dice(number)
                self.__btns_dice_roll[x] = die
                self.__btns_dice_held[x] = None

                if self.__btn_roll is not None:
                    # Disable Roll! button
                    self.__btn_roll['state'] = ['disabled']

        for x in self.__btns_dice_roll:  # Re-enable rolled dice
            if x is not None and x['text'] not in self.__rolls_kept:
                x['state'] = ['normal']

        self.__update_dice_points()

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

    def get_top_tile(self):
        if len(self.__tiles) > 0:
            return self.__tiles[-1]
        return None

    def get_victory_points(self):
        return int(self.__lbl_victory_pts['text'])

    def has_worms(self):
        for x in self.__btns_dice_held:
            if x is not None and x['text'] == 'W':
                return True

        return False

    def update_top_tile(self, tile):
        """ Updates the player's tile button to be the tile parameter.
        Adds the tile onto the player's collection of tiles.
        """
        self.btn_top_tile['text'] = tile['object']['text']
        self.btn_top_tile['state'] = 'disabled'
        if tile not in self.__tiles:
            self.__tiles.append(tile)
        else:
            self.__tiles.remove(tile)

    def __update_dice_points(self):
        """ Update dice points label and
        update grill status based on dice points.
            Returns dice point amount.
        """
        d_pts = 0
        for x in self.__rolls_kept:
            d_pts += 5 if x == 'W' else + x

        self.__lbl_dice_pts['text'] = f'({d_pts})'
        self.__board.update_grill_status(d_pts, self)

        return d_pts

    def __update_victory_points(self):
        points = 0
        for x in self.__tiles:
            points += x['points']

        self.__lbl_victory_pts['text'] = points

    def __turn_bust(self, bust_str):
        """A bust causes the top tile of the player's
        tile stack to be returned to the grill. If no tiles
        remain, the largest value grill tile is now out of play.
        """
        if len(self.__tiles) < 1:
            self.__board.remove_tile_from_play()
        else:
            self.remove_top_tile('grill')

        self.txt_notif.set(f'Busted!\n{bust_str}')
        self.end_turn()

    def remove_top_tile(self, new_location):
        removed_tile = self.__tiles.pop(-1)
        removed_tile['status'] = new_location
        removed_tile['object']['state'] = ['disabled']
        if len(self.__tiles) > 0:
            self.btn_top_tile['text'] = self.__tiles[-1]['object']['text']
        else:
            self.btn_top_tile['text'] = 'None'
        self.btn_top_tile['state'] = 'disabled'

        self.__update_victory_points()

    def end_turn(self):
        # Reset dice
        self.__btn_roll['state'] = ['disabled']
        for x in range(len(self.__btns_dice_held)):
            if self.__btns_dice_held[x] is not None:
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


class Player:
    def __init__(self):
        self.__board = None
        self.__tiles = []  # stores tiles gathered. most recent at top
        self.__rolls_kept = []  # stores numbers selected from rolls
        self.__lbls_dice_roll = []
        self.__lbls_dice_held = []
        self.__lbl_victory_pts = None
        self.__lbl_dice_pts = None
        self.btn_top_tile = None
        self.__btn_roll = None
        self.__busted = False
        self.txt_notif = StringVar()

    def set_player_objects(self, po_dictionary, board):
        self.__lbls_dice_roll = po_dictionary['dice roll']
        self.__lbls_dice_held = po_dictionary['dice held']
        self.__lbl_victory_pts = po_dictionary['points']
        self.__lbl_dice_pts = po_dictionary['dice points']
        self.btn_top_tile = po_dictionary['tile']
        self.__board = board

    def get_player_objects(self):
        """Objects to be accessed by a child instance
        """
        return {'board': self.__board, 'rolls kept': self.__rolls_kept,
                'busted': self.__busted, 'lbls roll': self.__lbls_dice_roll,
                'txt notif': self.txt_notif}

    def get_top_tile(self):
        if len(self.__tiles) > 0:
            return self.__tiles[-1]
        return None

    def get_victory_points(self):
        return int(self.__lbl_victory_pts['text'])

    def __get_ti_dice_cnt(self):
        """ Returns the total dice left in the roll and the
        invalid dice in the roll. Invalid dice are dice the
        player cannot select.
        """
        invalid_dice = 0
        total_dice = 0
        for x in self.__lbls_dice_roll:  # Check dice
            if x is not None:
                total_dice += 1
                if x['text'] in self.__rolls_kept:
                    invalid_dice += 1
        return invalid_dice, total_dice

    def activate_play(self):
        self.deactivate_busted()
        self.txt_notif.set('')
        self.end_turn()

    def deactivate_busted(self):
        self.__busted = False

    def roll_dice(self):
        """Randomly rolls dice between 1-6 for the player to select from.
        Dice that roll a 6 are indicated by a 'W' for worm.
        """
        num_dice = 8
        rolls = []
        for x in range(num_dice):
            rolls.append(random.randint(1, 6))

        # Change player GUI
        dice_buttons = self.__lbls_dice_roll
        for x in range(len(dice_buttons)):
            die = dice_buttons[x]
            roll_number = rolls[x]
            if rolls[x] == 6:
                roll_number = 'W'
            if die is not None:
                die['text'] = roll_number

        if self.__btn_roll is not None:
            self.__btn_roll['state'] = ['disabled']

        # Check if the player can choose from the roll
        invalid_dice, total_dice = self.__get_ti_dice_cnt()
        if invalid_dice == total_dice and total_dice != 0:
            self.turn_bust("No selectable dice.")

        return rolls

    def select_dice(self, number):
        """ Moves all dice of one number from the dice rolled row to the
        dice kept row.
        """
        for x in range(len(self.__lbls_dice_roll)):
            die = self.__lbls_dice_roll[x]

            if die is not None and number == die['text']:
                # Move dice to dice held
                self.__rolls_kept.append(number)
                die.grid(row=4)
                self.__lbls_dice_held[x] = self.__lbls_dice_roll[x]
                self.__lbls_dice_roll[x] = None

        d_pts = self.update_dice_points()
        self.__board.update_grill_status(d_pts, self)

        # Check if any tiles are selectable after there are no
        # more dice to roll.
        invalid_dice, total_dice = self.__get_ti_dice_cnt()
        if total_dice == 0:
            available_tile = False
            grill = self.__board.get_grill()
            for x in grill:
                if x['object']['state'] == 'normal':
                    available_tile = True
                    break
                elif x['val'] > d_pts:
                    break

            if not available_tile:
                self.turn_bust("Can't purchase any tiles.")

            elif not self.has_worms():
                self.turn_bust("You have no worms.")

    def has_worms(self):
        for x in self.__lbls_dice_held:
            if x is not None and x['text'] == 'W':
                return True

        return False

    def update_top_tile(self, tile):
        """ Updates the player's tile button to be the tile parameter.
        Adds the tile onto the player's collection of tiles.
        """
        self.btn_top_tile['text'] = tile['object']['text']
        self.btn_top_tile['state'] = 'disabled'
        if tile not in self.__tiles:
            self.__tiles.append(tile)
        else:
            self.__tiles.remove(tile)

    def update_dice_points(self):
        """ Update dice points label and
        update grill status based on dice points.
            Returns dice point amount.
        """
        d_pts = 0
        for x in self.__rolls_kept:
            d_pts += 5 if x == 'W' else + x

        self.__lbl_dice_pts['text'] = f'({d_pts})'
        return d_pts

    def __update_victory_points(self):
        points = 0
        for x in self.__tiles:
            points += x['points']

        self.__lbl_victory_pts['text'] = points

    def remove_top_tile(self, new_location):
        removed_tile = self.__tiles.pop(-1)
        removed_tile['status'] = new_location
        removed_tile['object']['state'] = ['disabled']
        if len(self.__tiles) > 0:
            self.btn_top_tile['text'] = self.__tiles[-1]['object']['text']
        else:
            self.btn_top_tile['text'] = 'None'
        self.btn_top_tile['state'] = 'disabled'

        self.__update_victory_points()

    def turn_bust(self, bust_str):
        """A bust causes the top tile of the player's
        tile stack to be returned to the grill. If no tiles
        remain, the largest value grill tile is now out of play.
        """
        if len(self.__tiles) < 1:
            self.__board.remove_tile_from_play()
        else:
            self.remove_top_tile('grill')

        self.txt_notif.set(f'Busted!\n{bust_str}')
        tksleep(2)
        self.__busted = True
        print("ENDING CASUAL TURN in [BUSTED]")
        self.end_turn()

    def end_turn(self):
        # Reset dice
        for x in range(len(self.__lbls_dice_held)):
            if self.__lbls_dice_held[x] is not None:
                self.__lbls_dice_roll[x] = self.__lbls_dice_held[x]
                self.__lbls_dice_roll[x].grid(row=3)
                self.__lbls_dice_held[x] = None

        for x in range(len(self.__lbls_dice_roll)):
            self.__lbls_dice_roll[x]['text'] = '/'

        self.__rolls_kept = []
        self.update_dice_points()
        self.__update_victory_points()
        self.__board.activate_next_player()


class CasualPlayer(Player):

    def __init__(self):
        super().__init__()
        self.__parent = super(CasualPlayer, self)
        self.__dice_options = []

    def activate_play(self):
        # Clean up before taking its turn
        self.deactivate_busted()
        self.get_player_objects()['txt notif'].set('')

        board = self.get_player_objects()['board']
        busted = self.get_player_objects()['busted']
        dice_points = self.update_dice_points()
        available_tiles = board.update_grill_status(dice_points, self)

        # roll until they can select a tile
        while (len(available_tiles) < 1) and (not busted):
            rolls = self.__parent.roll_dice()
            tksleep(1)
            self.__choose_dice(rolls)
            dice_points = self.__parent.update_dice_points()
            available_tiles = board.update_grill_status(dice_points, self)
            busted = self.get_player_objects()['busted']
            tksleep(1)

        if busted:  # Prevent a CPU from ending its turn twice
            return

        # select a tile
        tile_idx = int(available_tiles[-1]['val'])
        worms = board.pick_tile(self, tile_idx)

        # keep rolling until they get worms or bust
        while not busted and not worms:
            rolls = self.__parent.roll_dice()
            tksleep(1)
            self.__choose_dice(rolls)
            dice_points = self.__parent.update_dice_points()
            available_tiles = board.update_grill_status(dice_points, self)
            busted = self.get_player_objects()['busted']

            tksleep(1)
            if busted:
                return
            tile_idx = int(available_tiles[-1]['val'])
            worms = board.pick_tile(self, tile_idx)

        # turn end
        print("ENDING CASUAL TURN in [ACTIVE PLAY]")

    def __choose_dice(self, raw_rolls):
        rolls_kept = self.__parent.get_player_objects()['rolls kept']
        lbls_dice_rolls = self.__parent.get_player_objects()['lbls roll']
        self.__dice_options = []
        rolls = []

        for x in range(len(raw_rolls)):
            if lbls_dice_rolls[x] is not None:
                rolls.append(raw_rolls[x])

        for x in rolls:
            y = 'W' if x == 6 else x
            if x not in self.__dice_options and y not in rolls_kept:
                self.__dice_options.append(x)

        if len(self.__dice_options) < 1:
            self.__parent.turn_bust("No dice options.")
            return

        die = random.randint(1, 6)
        while die not in self.__dice_options:
            die = random.randint(1, 6)

        if die == 6:
            die = 'W'
        self.__parent.select_dice(die)
