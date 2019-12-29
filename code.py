import board
import displayio
import digitalio
import adafruit_imageload
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import time
import random
import sys
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
from gamepadshift import GamePadShift
import parameters

display = board.DISPLAY
# Load fonts
s_font = cwd+"/fonts/Arial-12.bdf"
m_font = cwd+"/fonts/Arial-16.bdf"
s_font = bitmap_font.load_font(s_font)
m_font = bitmap_font.load_font(m_font)
splash = displayio.Group(max_size=20)

# Button Constants
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)

pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

def display_directions():
    text_group = displayio.Group(max_size = 2)
    title_text = Label(m_font, max_glyphs = 15)
    title_text.x = 0
    title_text.y = 10
    title_text.color = 0x0F0FFF
    text_group.append(title_text)
    title_text.text = "Slider Puzzle"
    sub_text = Label(s_font, max_glyphs=128)
    sub_text.x = 0
    sub_text.y = 70
    sub_text.color = 0xFFFFFF
    text_group.append(sub_text)
    sub_text.text = """Press A for 3x3
Press B for 4x4
After win, press
START to play again """
    return text_group

def display_win():
    text_group = displayio.Group(max_size = 2)
    win_text = Label(m_font, max_glyphs = 15)
    win_text.x = 20
    win_text.y = 50
    win_text.color = 0xFF0000
    text_group.append(win_text)
    win_text.text = "YOU WON!"
    return text_group

def display_full_image():
    file_path = parameters.puzzle_graphics_folder + "/" + parameters.image["name"]
    with open(file_path, "rb") as f:
        odb = displayio.OnDiskBitmap(f)
        tile_grid = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter())
        splash.append(tile_grid)
        # Wait for the image to load.
        board.DISPLAY.wait_for_frame()
    return()

def solvable(tiles, size):
    """
    Check whether a sliding puzzle is solvable. For 3x3 or any odd dimension square puzzle,
    Checks the number of "inversions". If this is even then the puzzle configuration is solvable.
    An inversion is when two tiles are in the wrong order.
    For example, the sequence 1, 3, 4, 7, 0, 2, 5, 8, 6 has nine inversions:
    The empty tile (8) is ignored.
    Even dimension square puzzles are a bit more complicated. The puzzle is solvable if
    the blank is on an even row counting from the bottom (second-last, fourth-last, etc.)
    and number of inversions is odd OR
    the blank is on an odd row counting from the bottom and number of inversions is even.
    """
    count = 0
    if size == 3:
        for i in range(9):
            if tiles[i] != 8:
                for j in range(i+1, 9):
                    if tiles[i]  > tiles[j]:
                        count += 1
        return count % 2 == 0
    else:
        for i in range(16):
            if tiles[i] != 15:
                for j in range(i+1, 16):
                    if tiles[i]  > tiles[j]:
                        count += 1
        if int(tiles.index(15) / 4) in [0, 2]: # even rows from bottom
            return count % 2 != 0
        else:
            return count % 2 == 0

# Set state of game
# States are "intro", "setup", "play", "solved"
state = "intro" # State of Game
while True:
    if state == "intro":
        display.show(splash)
        display_full_image()
        # Display intro text
        directions = display_directions()
        splash.pop()
        splash.append(directions)
        # Select size of puzzle (3x3 or 4x4)
        current_buttons = pad.get_pressed()
        last_read = 0
        selected = False
        while selected == False:
            # Reading buttons too fast returns 0
            if (last_read + 0.1) < time.monotonic():
                buttons = pad.get_pressed()
                last_read = time.monotonic()
            if current_buttons != buttons:
                # Respond to the buttons
                if (buttons & BUTTON_A) > 0 :
                    size = 3
                    state = "setup"
                    selected = True
                elif (buttons & BUTTON_B) > 0:
                    size = 4
                    state = "setup"
                    selected = True
                current_buttons = buttons
        # set up lists for left, right, top bottom for checking valid moves
        if size == 3:
            top = [0, 1, 2]
            left = [0, 3, 6]
            right = [2, 5, 8]
            bottom = [6, 7, 8]
        else:
            top = [0, 1, 2, 3]
            left = [0, 4, 8, 12]
            right = [3, 7, 11, 15]
            bottom = [12, 13, 14, 15]
        splash.pop()

    if state == "setup":
        ### Scramble icons and display
        # Load and set up the tile grid for pieces
        if size == 3:
            file_path = parameters.puzzle_graphics_folder + "/" + parameters.image["tiles3"]
        else:
            file_path = parameters.puzzle_graphics_folder + "/" + parameters.image["tiles4"]
        bitmap, palette = adafruit_imageload.load(file_path,
                                                 bitmap=displayio.Bitmap,
                                                 palette=displayio.Palette)

        # Create TileGrids to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        # size = parameters.sizes[size_idx]
        if size == 3:
            tile_width = 53
            tile_height= 42
            solution = [i for i in range(0,9)]
        else:
            tile_width = 40
            tile_height= 32
            solution = [i for i in range(0,16)]
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette,
                                                width = size, height = size,
                                                tile_width = tile_width, tile_height= tile_height)
        # Set initial position of the pieces_bitmap
        for i in solution:
            tile_grid[i] = i
        splash.append(tile_grid)
        time.sleep(3)
        splash.pop()

        # Randomize the puzzle
        bad_puzzle = True
        while bad_puzzle:
            #generate random
            pieces_count = size * size
            pieces = []
            temp_array = solution.copy()
            for i in solution:
                j = random.randint(0,len(temp_array)-1)
                pieces.append(temp_array[j])
                del temp_array[j]
            bad_puzzle = not solvable(pieces, size)
        for i in pieces:
            tile_grid[i] = pieces[i]
        splash.append(tile_grid)
        state = "play"
    # Get button input, adjust image, check for win
    current_buttons = pad.get_pressed()
    last_read = 0
    while state == "play":
    #   Reading buttons too fast returns 0
        if (last_read + 0.1) < time.monotonic():
            buttons = pad.get_pressed()
            last_read = time.monotonic()
        if current_buttons != buttons:
    #      Respond to the buttons
            if size == 3:
                blank = pieces.index(8)
                blank_number = 8
            else:
                blank = pieces.index(15)
                blank_number = 15
            if (buttons & BUTTON_LEFT) > 0 :
                if blank not in right:
                    pieces[blank] = pieces[blank+1]
                    pieces[blank+1] = blank_number
            elif (buttons & BUTTON_RIGHT) > 0:
                if blank not in left:
                    pieces[blank] = pieces[blank-1]
                    pieces[blank-1] = blank_number
            elif (buttons & BUTTON_UP) > 0:
                if blank not in bottom:
                    pieces[blank] = pieces[blank+size]
                    pieces[blank+size] = blank_number
            elif (buttons & BUTTON_DOWN) > 0:
                if blank not in top:
                    pieces[blank] = pieces[blank-size]
                    pieces[blank-size] = blank_number
            current_buttons = buttons
        for i in pieces:
            tile_grid[i] = pieces[i]
        splash.pop()
        splash.append(tile_grid)
        if pieces == solution:
            state = "solved"

    # If win, display "you won"
    splash.pop()
    splash.append(display_win())
    time.sleep(3)
    splash.pop()
    display_full_image()
    while state == "solved":
    # Check if start pressed, in which case, go back to state = setup
    # Get button input, adjust image, check for win
        current_buttons = pad.get_pressed()
        last_read = 0
    #   Reading buttons too fast returns 0
        if (last_read + 0.1) < time.monotonic():
            buttons = pad.get_pressed()
            last_read = time.monotonic()
        if current_buttons != buttons:
            # Respond to the buttons
            blank = pieces.index(8)
            if (buttons & BUTTON_START) > 0 :
                splash.pop()
                state = "intro"
            current_buttons = buttons