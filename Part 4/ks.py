#!/usr/bin/env python3

import sys, os, argparse
import time, random
import wave, math, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

# Show a plot of the algorithms in action?
gShowPlot = False

"""
Notes of a pentatonic minor scale
Piano C4, E flat, F, G, B flat, C5
Root, Third flat, Fourth, Fifth, Seventh Flat, Octave
Semitone Interval = [0 (Root), 3, 5, 7, 10, 12]
"""
pmNotes = {
   'C4': 262,
   'Eb': 311,
   'F': 349,
   'G': 391,
   'Bb': 466
}

def writeWAVE(fname, data):
   
   # Open the file
   with wave.open(fname, 'wb') as file:
      # WAV file parameters
      nChannels = 1
      sampleWidth = 2
      frameRate = 44100
      nFrames = 44100
      
      # Now set the parameters
      file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
      file.writeframes(data)

def generateNote(freq):
   numSamples = 44100
   sampleRate = 44100
   N = int(sampleRate/freq)
   
   # Initialize the ring buffer
   buf = deque([random.random() - 0.5 for i in range(N)])
   
   # Plot of flag set
   if gShowPlot:
      axline, = plt.plot(buf)
   
   #Initialize the samples buffer
   samples = np.array([0]*numSamples, 'float32')
   for i in range(numSamples):
      samples[i] = buf[0]
      # print(f'{samples[0]} = Samples\n {buf[0]} = Buffer\n')
      avg = 0.996*0.5*(buf[0] + buf[1])
      buf.append(avg)
      buf.popleft()
      
      # Plot of flag set
      if i % 1000 == 0:
         axline.set_ydata(buf)
         plt.draw()
   
   # Convert samples to 16 bit values, and then to a string
   # The maximum value is 32767 for an unsigned 16 bit integer
   samples = np.array(samples*32767, 'int16')
   return samples.tostring()


sampleRate = 44100
numSamples = sampleRate*5
x = np.arange(numSamples)/float(sampleRate)
vals = np.sin(2.0*math.pi*220.0*x)
data = np.array(vals*32767, 'int16').tostring()
with wave.open('sine220.wav', 'wb') as file:
   file.setparams((1, 2, sampleRate, numSamples, 'NONE', 'uncompressed'))
   file.writeframes(data)

# Here we implement the Karpus Strong algorithm
# Generate a note of a given frequency

      
# Play a WAV file
class NotePlayer:
   
   # Constructor
   def __init__(self):
      pygame.mixer.pre_init(44100, -16, 1, 2048)
      pygame.init()
      
      # A dictionary of notes
      self.notes = {}
      
   # Add a note
   def add(self, fileName):
      self.notes[fileName] = pygame.mixer.Sound(fileName)
   
   # Play a note
   def play(self, fileName):
      try:
         self.notes[fileName].play()
      except:
         print(f'Error type {e}.  {fileName} not found!')
   
   def playRandom(self):
      
      # Play a random note
      index = random.randint(0, len(self.notes)-1)
      note = list(self.notes.values())[index]
      note.play()

# The main() function
def main():

   # Declare global variables
   global gShowPlot

   parser = argparse.ArgumentParser(description="Generating random sounds on the pentatonic scale using the Karpus Strong algorithm")

   # Add arguments
   parser.add_argument('--display', '--d', action='store_true', required=False)
   parser.add_argument('--play', '--p', action='store_true', required=False)
   parser.add_argument('--piano', '--o', action='store_true', required=False)
   args = parser.parse_args()

   # Show the plot if the flag is set
   if args.display:
      gShowPlot = True
      plt.ion()

   # Create the note player
   nplayer = NotePlayer()

   print('Creating notes...')
   for name, freq in list(pmNotes.items()):
      fileName = name + '.wav'
      if not os.path.exists(fileName) or args.display:
         data = generateNote(freq)
         print(f'Creating {fileName}...')
         writeWAVE(fileName, data)
      else:
         print(f'{fileName} already exists.  Skipping to next file...')
      
      # Add a note to the player
      nplayer.add(name + '.wav')
   
      # Play a note if the display flag is set
      if args.display:
         nplayer.play(name + '.wav')
         time.sleep(0.5)
   
   # Play a random tune
   if args.play:
      while True:
         try:
            nplayer.playRandom()
         
            # Rest - 1 to 8 beats
            rest = np.random.choice([1, 2, 4, 8], 1, p = [0.15, 0.7, 0.1, 0.05])
            time.sleep(0.25*rest[0])
         except KeyboardInterrupt as e:
            exit()
         
   # Random piano mode
   if args.piano:
      while True:
         for event in pygame.event.get():
            if (event.type == pygame.KEYUP):
               print("Key pressed")
               nplayer.playRandom()
               time.sleep = 0.5

# Call the main function
if __name__ == '__main__':
   main()