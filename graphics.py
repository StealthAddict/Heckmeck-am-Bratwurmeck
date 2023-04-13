from tkinter import *
from tkinter import ttk
# from main import Board, Player

"""
I want a 3x3 grid of labels in which I can place my grill,
and player stations.
"""
def create_label_frames(root):
    main_frame = ttk.Frame(root, padding='1 1 1 1')
    main_frame.grid(row=1, column=1)
    frames = []
    for row in range(3):
        frame_row = []
        for col in range(3):
            frame = LabelFrame(main_frame)
            frame.grid(row=row, column=col, sticky='ew')
            frame_row.append(frame)
        frames.append(frame_row)
    
    return frames

# TODO: could later make the main_player argument a list with the # players selected
def create_player_labels(frames, main_player, board):
     # set up player stations
    p1 = generate_player_mat(2, 1, frames, main_player)
    main_player.set_player_objects(p1)
    generate_player_mat(1, 0, frames, None)  # left
    generate_player_mat(0, 1, frames, None)  # top
    generate_player_mat(1, 2, frames, None)  # right
    board.set_grill_tiles(generate_grill(1, 1, frames))



def generate_player_mat(row, col, frames, main_player):
    player_frame = frames[row][col]
    empty_button = Button(player_frame, text='/', state=['disabled'])

    # Text labels
    Label(player_frame, text='Points:').grid(row=0, column=0)
    Label(player_frame, text='Top Tile:').grid(row=1, column=0)
    Label(player_frame, text='Dice\nRolled:').grid(row=2, column=0)
    Label(player_frame, text='Dice Held:').grid(row=3, column=0)

    # Counters/dice
    points = Label(player_frame, text='0')
    points.grid(row=0, column=1)
    tiles = Label(player_frame, text='None')  # Only ever shows top most tile
    tiles.grid(row=1, column=1)
    dice_roll = []
    for x in range(8): 
        die = Button(player_frame, text='/', state=['disabled'],
                     height='1', width='1')
        die.grid(row=2, column=x+1)        
        dice_roll.append(die)
    
    player_objects = {'points': points, 'tiles': tiles, 'dice roll': dice_roll,
                      'dice held': [None, None, None, None, None, None,
                                    None, None]} 

    if main_player: 
        roll_dice = Button(player_frame, text='Roll!', 
                           command=lambda: main_player.roll_dice(), 
                           state=['normal'])
        roll_dice.grid(row=4, column=0)
        player_objects['button'] = roll_dice


    return player_objects


def generate_grill(row, col, frames):
    grill_frame = frames[row][col]
    grill_tiles = []

    title_label = Label(grill_frame, text='GRILL')
    title_label.grid(row=0, columnspan=(4))

    point_val = 1
    col = 0
    for x in range(21, 37):
            bratwurm_tile = Button(grill_frame, text=f'{x} Worms\n{point_val} Pts')
            bratwurm_tile.grid(row=point_val, column=col)
            grill_tiles.append(bratwurm_tile)

            if x % 4 == 0: point_val += 1

            col = 0 if col == 3 else col + 1

    return grill_tiles
