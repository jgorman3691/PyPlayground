#!/usr/bin/env python3


def findDuplicates(fileName):
    print(f'Finding duplicate tracks in {fileName}...')

    # Read in a playlist
    with open(fileName, 'r') as plist:
        plist = plistlib.readPlist(fileName)

    # Get the tracks from the Tracks dictionary
    tracks = plist['Tracks']

    # Create a track name directory
    trackNames = {}

    # Iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']

            # Look for existing entries
            if name in trackNames:
                # If a name and duration match, increment the count, rounding the track length to the nearest second
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)
                else:
                    # Add the dictionary entry as a tuple (duration, count)
                    trackNames[name] = (duration, 1)

        except:
            # Ignore
            pass

    # Store the duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))

    # Save the duplicates to a file
    if len(dups) > 0:
        print(f"Found {len(dups)} duplicates.  track names saved to dup.txt")
    else:
        print("No duplicate tracks found!")

    with open("dups.txt", "w") as f:
        for val in dups:
            f.write(f"[{val[0]}] {val[1]}\n")
