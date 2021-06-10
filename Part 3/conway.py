#!/usr/bin/env python3

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as an

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
   """
   Returns a grid of NxN random values.
   """
   return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
   # Adds a glider with its top left cell at (i, j)
   glider = np.array([[0, 0, 255],
                     [255, 0, 255],
                     [0, 255, 255]])
   grid[i:i+3, j:j+3] = glider

def addGosper(i, j, grid):
   # Adds a Gosper Gun with its top left at (i, j)
   gun = np.zeros(11*38).reshape(11, 38)
   gun[1][25] = 255
   gun[2][23] = gun[2][25] = 255
   gun[3][13] = gun[3][14] = gun[3][21] = gun[3][22] = gun[3][35] = gun[3][36] = 255
   gun[4][12] = gun[4][16] = gun[4][21] = gun[4][22] = gun[4][35] =  gun[4][36]
   gun[5][1] = gun[5][2] = gun[5][11] = gun[5][17] = gun[5][22] = gun[5][23] = 255
   gun[6][1] = gun[6][2] = gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = gun[6][23] = gun[6][25] = 255
   gun[7][11] = gun[7][17] = gun[7][25] = 255
   gun[8][12] = gun[8][16] = 255
   gun[9][13] = gun[9][14] = 255
   grid[i:i+11, j: j+38] = gun

def update(frameNum, img, grid, N):
   """
   Copy the grid since we require 8 neighbors for the calculation, and we go line by line
   """
   newGrid = grid.copy()
   for i in range(N):
      for j in range(N):
         """
         Compute the 8 neighbor sum using toroidal boundary conditions.
         x and y wrap around so that the sim takes place on a toroid
         """
         total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                     grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                     grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                     grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
         # Apply Conway's Rules
         if grid[i, j] == ON:
            if(total < 2) or (total > 3):
               newGrid[i, j] = OFF
         else:
            if total == 3:
               newGrid[i, j] = ON
               
   # Update the data
   img.set_data(newGrid)
   grid[:] = newGrid[:]
   return img,

# Main Function
def main():
   """
   Command line arguments are in sys.argv[n]
   sys.argv[0] is the script name and can be ignored
   """
   # Parse arguments
   parser = argparse.ArgumentParser(description="Runs Conway's Game of Life.  Topology is toroidal")
   
   # Add arguments
   parser.add_argument('--grid-size', '-g', dest='N', required=False)
   if('--grid-size' or '-g') == False:
      parser.add_argument('--horizontal', '-w', dest='horizontal', required=False)
      parser.add_argument('--vertical', '-v', dest='vertical', required=False)
   parser.add_argument('--mov-file', '-m', dest='movfile', required=False)
   parser.add_argument('--interval', '-i', dest='interval', required=False)
   parser.add_argument('--glider', '-l', action='store_true', required=False)
   parser.add_argument('--gosper', '-r', action='store_true', required=False)
   args = parser.parse_args()
   
   # Set grid size
   N = 100
   if args.N and int(args.N) > 38:
      N = int(args.N)
   
   # Set the animation update interval
   updateInterval = 10
   if args.interval:
      updateInterval = int(args.interval)
   
   # Declare Grid
   grid = np.array([])
   
   # Check if the "glider" demo flag is specified
   if args.glider:
      grid = np.zeros(N*N).reshape(N,N)
      addGlider(1, 1, grid)
   else:
      # Populate the grid with off and on values...more off than on
      grid = randomGrid(N)
   
   # Check if the "gosper" demo flag is specified
   if args.gosper:
      if args.vertical:
         vertical = int(args.vertical)
      if args.horizontal:
         horizontal = int(args.horizontal)
      try:
         if (horizontal > 38) or (vertical > 11) and N not in int(N.args):
            grid = np.zeros(horizontal*vertical).reshape(horizontal,vertical)
            addGosper(1, 1, grid)
      except Exception:
         print("Grid size too small.")
         grid = randomGrid(N)
         
   else:
      grid = randomGrid(N)
   # Set up the animation
   fig, ax = plt.subplots()
   img = ax.imshow(grid, interpolation='nearest')
   ani = an.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                          frames=10,
                          interval=updateInterval,
                          save_count=1000)
   
   # Number of frames?
   # Set the output file
   if args.movfile:
      ani.save(args.movfile, fps=30, extra_args=[-'-vcodec','libx264'])
   
   plt.show()

# Call main
if __name__ == '__main__':
   main()