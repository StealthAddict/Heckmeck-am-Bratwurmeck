from tkinter import *
from graphics import *
from players import *

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
    main_player = MainPlayer() # Human-controlled player
    players = [main_player, CasualPlayer(), Player(), Player()]
    frames = create_label_frames(root)
    create_player_labels(frames, players, board)

    board.assign_players(players)
    root.mainloop()
    pass


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