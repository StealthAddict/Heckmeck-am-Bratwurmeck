from tkinter import *
from graphics import *
from players import *

def main():
    root = Tk()
   
    root.title('Heckmeck am Bratwurmeck')
    root.resizable(False, False)
    root.config(bg='White')
    board = Board()
    main_player = MainPlayer() # Human-controlled player
    players = [main_player, CasualPlayer(), Player(), Player()]
    frames = create_label_frames(root)
    create_game_labels(frames, players, board)
    board.assign_players(players)

    root.mainloop()
    pass


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
        """
        for x in range(len(self.__grill)):
            if self.__grill[x] is not None:
                if self.__grill[x]['status'] == 'grill':
                    if self.__grill[x]['val'] <= dice_pts:
                        self.__grill[x]['object']['state'] = ['normal']
                    elif self.__grill[x]['val'] > dice_pts:
                        self.__grill[x]['object']['state'] = ['disabled']  

                elif self.__grill[x]['val'] == dice_pts and self.__grill[x]['status'] != 'OOP':
                    player = self.__grill[x]['status']
                    player._btn_top_tile['state'] = ['normal']

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
            self.txt_notif.set("You don't have any worms!")
            invalid_dice, total_dice = player.get_ti_dice_cnt()
            if total_dice == 0:
                print("worm bust")
                player.turn_bust()

    def assign_players(self, player_list):
        self.__players = player_list

    def activate_next_player(self):
        """Signals the next player to begin their turn if the game
        has not ended.
        """
        if not self.__game_over:
            self.__players[self.__next_player].activate_play()
            self.__next_player = 0 if self.__next_player == 3 else + 1
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

if __name__ == '__main__':
    main()