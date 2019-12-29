# PyBadge-Sliding-Puzzle
Sliding puzzle for PyBadge and PyBadge LC

This software is for the Adafruit PyBadge or PyBadge LC and is written in CircuitPython. It's a sliding puzzle game, and lets the user select either a 3x3 or 4x4 puzzle. As described below, the parameters file can be changed to select different puzzle images, and you can create your own. 

## How to Play the Game
To play, simply load the software onto the PyBadge and turn it on. The display will first show the complete puzzle image, and then will ask you to press the "A" button for a 3x3 (8 tile) puzzle or the "B" button for a 4x4 (15 tile) puzzle. One slot is always empty so that tiles can be moved. Once you have made your selection, you'll see the puzzle image with the pieces, in the solved state, and then the puzzle will be scrambled for play. The 4x4 puzzle is significantly harder than the 3x3 puzzle and will take more moves to solve, but both are fairly easy with practice.

Use the 3 directional buttons to slide a tile at a time. The goal is to get the tiles arranged in numerical order, left to right and top to bottom, with the empty spot on the bottom right. Once you have done this, you win! After the complete image is displayed upon winning, you can press the START button to play again. Sometimes you need to press the button a couple of times.

Stuck? There are a number of heuristics for humans to use to solve these puzzles (as well as heuristic algorithms for computers). The approach that works for me is documented here.

## Changing the Puzzle Images and Creating Your Own
The parameters.py file stores several parameters, including the name of the folder where the puzzle images are stored. To change, for example, from the Santa to the witch puzzle, simply edit the line: puzzle_graphics_folder = "santa" to puzzle_graphics_folder = "witch". I have provided three sets of images for the puzzle: Santa, a witch, and a Valentine's Day floral image.

To make your own puzzles, you need to create 3 bmp images:

The full image, to be saved as "full.bmp" in a new folder
A tile image for the 3x3 puzzle, to be saves as "tiles3.bmp" in the same folder
A tile image for the 4x4 puzzle, to be saved as "tiles4.bmp" in the same folder. .

These images must be exactly the right size in order for the program to work. The full image and 4x4 tile image must be 160 pixels wide by 128 pixels high. The 3x3 itile image must be 159 pixels wide by 126 pixels high.

Start from the full image. To make the 4x4 tile image, black out the pixels on the lower right of the image (x coordinates 121 - 160, y coordinates 96 - 128). You can also put numbers on what will be each tile to make solving the puzzle easier To do this, I use an image editing program to add a layer with a set of grid lines creating a 4x4 grid. Then I blacken out the lower right tile and put numbers in the upper right of each tile. Then I delete the grid layer and save the image as a bmp file. Follow the same process for the 3x3 tile image, but first re-scale the total image to be 159 x 126 and use a 3x3 rather than 4x4 grid. Once you have saved the three files in a new folder, change the puzzle_graphics_folder line in the parameters.py program to point to the new folder name.
