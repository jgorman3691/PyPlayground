#!/usr/bin/env python3

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