#!/usr/bin/env python3

import re, argparse, sys
import matplotlib.pyplot as plt
import plistlib
import numpy as np

def findCommonTracks(fileNames):
   
   # A list of sets of Track names
   trackNameSets = []
   for fileName in fileNames:
      
      # Create a new set
      trackNames = set()
      
      # Read in the playlist
      plist = plistlib.readPlist(fileName)
      
      # Get the tracks
      tracks = plist['Tracks']
      
      # Iterate through the tracks
      for trackId, track in tracks.items():
         try:
            # Add the Track name to a set (if the name exists)
            trackNames.add(track['Name'])
         except:
            # Ignore and get the set of common tracks
            pass
      
         # Now add them to a list
         trackNameSets.append(trackNames)
      
   # Get the set of common tracks
   commonTracks = set.intersection(*trackNameSets)
      
   #Now write to a file
   if len(commonTracks) > 0:
      with open("common.txt", "w") as f:
         for val in commonTracks:
            s = (f"{val}\n")
            f.write(s.encode("UTF-8"))
      print(f"{len(commonTracks)} common tracks were found.\nTrack names have been written to common.txt.")
   else:
      print("No common tracks!")

def plotStats(fileName):
   
   # Read in a playlist, and get the tracks from the playlist
   plist = plistlib.readPlist(fileName)
   tracks = plist['Tracks']
   
   # Iterate through the tracks after creating lists of song ratings and Track durations
   ratings = []
   durations = []
   for trackId, track in tracks.items():
      try:
         ratings.append(track['Album Rating'])
         durations.append(track['Total Time'])
      except:
         pass
   
   # Ensure that valid data was collected
   if ratings == [] or durations == []:
      print(f"No valid Album Rating/Total Time data in {fileName}.")
      return

   # Scatter Plot
   x = np.array(durations, np.int32)
   
   #Convert to minutes
   x = x/60000.0
   y = np.array(ratings, np.int32)
   
   plt.subplot(2, 1, 1)
   plt.plot(x, y, 'o')
   plt.axis([0, 1.05*np.max(x), -1, 110])
   plt.xlabel('Track Duration')
   plt.ylabel('Track Rating')
   
   # Plot histogram
   plt.subplot(2, 1, 2)
   plt.hist(x, bins=20)
   plt.xlabel('Track Duration')
   plt.ylabel('Count')
   
   # Show plot
   plt.show()
   

def findDuplicates(fileName):
   print(f'Finding duplicate tracks in {fileName}...')
   
   # Read in a playlist
   with open(fileName, 'r') as plist:
      plist = plistlib.readPlist(fileName)
      
   # Get the tracks from the Tracks dictionary
   tracks = plist['Tracks']
   
   # Create a Track name directory
   trackNames = {}
   
   # Iterate through the tracks
   for trackId, track in tracks.items():
      try:
         name = track['Name']
         duration = track['Total Time']
         # Look for existing entries
         if name in trackNames:
            if duration//1000 == trackNames[name][0]//1000:
               # Add the dictionary entry as a tuple (duration, count)
               trackNames[name] = (duration, 1)
      except:
         # Ignore
         pass
   
   # Store the duplicates as (name, count) tuples
   dups = []
   for k, v in trackNames.items():
      if v[1] > 1:
         dups.append((v[1],k))
   
   # Save the duplicates to a file
   if len(dups) > 0:
      print(f"Found {len(dups)} duplicates.  Track names saved to dup.txt")
   else:
      print("No duplicate tracks found!")
   
   with open("dups.txt", "w") as f:
      for val in dups:
         f.write(f"[{val[0]}] {val[1]}\n")

# Now we gather the code inside the main function
def main():
   
   # Create parser
   descStr = """
   This program analyzes playlist files in (.xml) format, exported from iTunes.
   """
   
   
   parser = argparse.ArgumentParser(description=descStr)
   
   # Add a mutually exclusive group of arguments
   group = parser.add_mutually_exclusive_group()
   
   # Add the expected arguments
   group.add_argument('--common', nargs='*', dest='plFiles', required=False)
   group.add_argument('--stats', dest='plFile', required=False)
   group.add_argument('--dup', dest='plFileD', required=False)
   
   # Parse args
   args = parser.parse_args()
   
   if args.plFiles: # Find common tracks
      findCommonTracks(args.plFiles)
   elif args.plFile: # Plot Stats
      plotStats(args.plFile)
   elif args.plFileD: # Find Duplicate Tracks
      findDuplicates(args.plFileD)
   else:
      print("These are not the tracks you're looking for...\n")

# Main Method
if __name__ == '__main__':
   main()