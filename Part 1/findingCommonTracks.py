#!/usr/bin/env python3

def findCommonTracks(fileNames):
   
   # A list of sets of track names
   trackNameSets = []
   for fileName in fileNames:
      
      # Create a new set
      trackNames = set()
      
      # Read in the playlist, get the tracks, iterate through the tracks, and add to the list
      plist = plistlib.readPlist(fileName)
      tracks = plist['Tracks']
      for trackId, track in tracks.items():
         try:
            # Add the track name to a set (if the name exists)
            trackNames.add(track['Name'])
         except:
            # Ignore
            pass
      
      #  Add these to  list, and get the set of common tracks
      trackNameSets.append(trackNames)
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