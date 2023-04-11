from tkinter import *
from tkinter import ttk

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
    
    # set up player stations, will need to apply them to the players so they can change them
    # TODO: add Player object to gen_mats; might just have create_label_frames return the dictionaries for the player and board
    generate_player_mats(0, 1, frames)  # top
    generate_player_mats(1, 0, frames)  # left
    generate_player_mats(1, 2, frames)  # right
    generate_player_mats(2, 1, frames)  # bottom
    
    # Set up grill
    grill = generate_grill(1, 1, frames)  # TODO: add to Board class

    return grill

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
            # Calculate point value
            if x % 4 == 0: point_val += 1

            col = 0 if col == 3 else col + 1

    return grill_tiles



def generate_player_mats(row, col, frames):
    player_frame = frames[row][col]

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

    # TODO: Only real player's dice should be clickable
    for x in range(8):
        # NTS: enable with '!disabled'
        die = Button(player_frame, text='/', command=lambda: print_1(),
                      state=['disabled'], height='1', width='1')
        die.grid(row=2, column=x+1)
        dice_roll.append(die)
    
    dice_held = []

    if True: # TODO: change to if real player
        roll_dice = Button(player_frame, text='Roll!', 
                           command=lambda: print_1(), state=['disabled'])
        roll_dice.grid(row=4, column=0)


    # TODO: add to player?


def print_1():
    print(1)