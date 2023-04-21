from tkinter import *
import tkinter as tk
from graphics import *
from players import *

def main():
    player_selection = Tk()
    player_selection.title('Heckmeck am Bratwurmeck')
    player_selection.resizable(False, False)
    create_player_selection(player_selection)
    # tk.Misc.tksleep = tksleep
    player_selection.mainloop()


class Board:
    def __init__(self):
        self.__grill = [] # all available tiles on the board in ascending order.
        self.__players = [] # list of Player objects playing the game
        self.__next_player = 0  # index of next player
        self.__game_over = False
        self.txt_notif = StringVar()

    def update_grill_status(self, dice_pts):
        """Update the button states of the grill's and players' top tiles
        according to the current roll points (dice_pts) of the player.
            Returns all available tiles to current player.
        """
        available_tiles = []
        for x in range(len(self.__grill)):
            if self.__grill[x] is not None:
                if self.__grill[x]['status'] == 'grill':
                    if self.__grill[x]['val'] <= dice_pts:
                        self.__grill[x]['object']['state'] = ['normal']
                        available_tiles.append(self.__grill[x])
                    elif self.__grill[x]['val'] > dice_pts:
                        self.__grill[x]['object']['state'] = ['disabled']  

                elif self.__grill[x]['val'] == dice_pts and self.__grill[x]['status'] != 'OOP':
                    player = self.__grill[x]['status']
                    if player.get_top_tile() == self.__grill[x]:
                        player._btn_top_tile['state'] = ['normal']
                        available_tiles.append(self.__grill[x])

        return available_tiles

    def set_up_grill(self, grill_tiles):
        """ Reset the grill for a new game.
        Replaces all 16 tiles in the grill.
        self.__grill: 'val' - the value needed to acquire the tile
            'points' - the # of points awarded by the tile
            'status' - where the tile currently is
            'object' - the tkinter Button
        """
        self.__grill = []
        point_val = 1
        for x in range(21, 37):
            self.__grill.append({'val': x, 'points': point_val,
                                 'status': 'grill', 
                                 'object': grill_tiles[x - 21]})
            
            # Calculates the correct point values for each tile
            if x % 4 == 0:
                point_val += 1

    def pick_tile(self, player, tile_idx):
        """To be used by tile buttons to move a tile (tile_idx)
        from the grill to a player. Player is unable to choose
        a tile if they have no worm dice, indicated by W.
        """
        if player.has_worms():
            tile = self.__grill[tile_idx - 21]
            player.update_top_tile(tile)
            player.end_turn()

            self.__grill[tile_idx - 21]['status'] = player
            self.__grill[tile_idx - 21]['object']['state'] = ['disabled']
        else:
            player.txt_notif.set("You don't have any worms!")

    def assign_players(self, player_list):
        self.__players = player_list

    def activate_next_player(self):
        """Signals the next player to begin their turn if the game
        has not ended.
        """
        if not self.__game_over:
            if self.__next_player == 3:
                self.__next_player = 0 
            else:
                self.__next_player += 1
                
            print(f'ACTIVATE PLAYER {self.__next_player + 1}')
            self.__players[self.__next_player].activate_play()
            self.set_notification(f'Player {self.__next_player + 1}\'s turn!')

    def set_notification(self, new_string):
        self.txt_notif.set(new_string)        

    def remove_tile_from_play(self):
        """Disable the highest value tile on the grill
        from play.
        """
        for x in range(len(self.__grill), 0):
            if self.__grill[x]['status'] == 'grill':
                self.__grill[x]['status'] = 'OOP'  # Out Of Play
                self.__grill[x]['object']['state'] = 'disabled'

                if self.__grill[x]['val'] == 21:
                    self.game_over('No tiles left on the grill.')

                break

    def game_over(self, end_condition):
        """Ends the game. end_condition is a string 
        that specifies why the game ended.
        """
        self.__game_over = True
        self.txt_notif.set(f'GAME OVER\n{end_condition}')

    def get_grill(self):
        return self.__grill


def create_player_selection(root):
    # Creates the initial window asking for player count.
    
    frame = Frame(root)
    frame.grid(row=0, column=0)

    title = Label(frame, text='Choose number of players to start.')
    title.grid(row=1, column=1, columnspan=5, padx=5, pady=5)

    option_selected = StringVar()
    
    radio_p2 = Radiobutton(frame, width=15, value=2, text='2 Players', 
                           variable=option_selected)
    radio_p2.grid(row=2, column=1)
    radio_p2.focus_set()
    radio_p3 = Radiobutton(frame, width=15, value=3, text='3 Players', 
                           variable=option_selected)
    radio_p3.grid(row=3, column=1)
    radio_p4 = Radiobutton(frame, width=15, value=4, text='4 Players', 
                           variable=option_selected)
    radio_p4.grid(row=4, column=1)

    Button(frame, text='finished', command=lambda : open_main_window(root, option_selected)).grid(row=5, column=2)


def open_main_window(prev_win, num_players):
    # Generates the main game window
    prev_win.destroy()
    root = Tk()
    root.title('Heckmeck am Bratwurmeck')
    root.resizable(False, False)
    
    board = Board()
    main_player = MainPlayer() # Human-controlled player

    if num_players.get() == '':
        num_players = 2
    else:
        num_players = int(num_players.get())

    players = [main_player, CasualPlayer(), Player(), Player()]
    for x in range(1, num_players):
        players[x] = CasualPlayer()
    board.assign_players(players)

    frames = create_label_frames(root)
    create_game_labels(frames, players, board)


def tksleep(t):
    """A function to emulate time.sleep in tkinter created
    by Thingmabobs on StackOverflow 
    https://stackoverflow.com/a/74162322
    """
    'emulating time.sleep(seconds)'
    ms = int(t*1000)
    root = tk._get_default_root('sleep')
    var = tk.IntVar(root)
    root.after(ms, var.set, 1)
    root.wait_variable(var)


if __name__ == '__main__':
    main()