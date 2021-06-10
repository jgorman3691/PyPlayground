#!/usr/bin/env python3

def plotStats(fileName):

   # Read in a playlist, and get the tracks from the playlist
   plist = plistlib.readPlist(fileName)
   tracks = plist['Tracks']

   # Iterate through the tracks after creating lists of song ratings and track durations
   ratings = []
   durations = []
   for trackId, track in tracks.items():
      try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
      except:
            # Ignore
            pass

   # Ensure that valid data was collected
   if ratings == [] or durations == []:
      print(f"No valid Album Rating/Total Time data in {fileName}")
      return

# Scatter Plot
x = np.array(durations, np.int32)

#Convert to minutes
x = x / 60000.0
y = np.array(ratings, np.int32)

pyplot.subplot(2, 1, 1)
pyplot.plot(x, y, 'o')
pyplot.axis([0, 1.05 * np.max(x), -1, 110])
pyplot.xlabel('Track Duration')
pyplot.ylabel('Track Rating')

# Plot histogram
pyplot.subplot(2, 1, 2)
pyplot.hist(x, bins=20)
pyplot.xlabel('Track Duration')
pyplot.ylabel('Count')

# Show plot
pyplot.show()