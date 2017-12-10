#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import wave
import numpy as np
import pygame
from scipy import signal

#maximal sound amplitude and sampling rate
MAXAMP = 16383
SAMPLERATE = 48000

#Mono
NCHANNELS = 1

# sound length (seconds) and frequency (Herz)
SOUNDLEN = 0.417
SOUNDFREQ = 333.3

# calculate the total amount of cycles
ncycles = SOUNDLEN * SOUNDFREQ

# calculate the total amount of samples
nsamples = SOUNDLEN * SAMPLERATE

# calculate samples per cycle
spc = nsamples / ncycles

# stepsize is the distance between samples within a cycle
stepsize = (2*np.pi) / spc

# create a range of numbers between 0 and 2*pi
x = np.arange(0, 2*np.pi, stepsize)

# make a sine wave out of the range
sine = np.sin(x)

# increase the amplitude
sine = sine * MAXAMP

# repeat the sine wave
allsines = np.tile(sine, int(ncycles))

# calculate asymmetric Hanning vector (22ms rise and 394 fall)
riseLen = nsamples / 19        #0.022 * SAMPLERATE
fallLen = nsamples - riseLen         #.394 * SAMPLERATE
# create Hann vector for rise len * 2
riseVec = np.hanning((riseLen * 2))
# delete second half of vector (after 1.0)
riseVec = riseVec[0:int(riseLen)]

# create Hann vector for fall len * 2
fallVec = np.hanning((fallLen * 2))
# delete first half of vector
fallVec = fallVec[int(fallLen):]
# combine vectors
hannVec = np.concatenate((riseVec, fallVec),)

if len(hannVec) > len(allsines):
    hannVec = hannVec[0:len(allsines)]

# apply Hanning amplitude modulation
allsines = allsines * hannVec

# multiply beats
beats = np.tile(allsines, 79)

# initialise mixer module (it requires the sampling rate and num of channels)
pygame.mixer.init(frequency=SAMPLERATE, channels=NCHANNELS)

# create sound out of the allsines vector
tone = pygame.mixer.Sound(beats.astype('int16'))

# open new wave file objects
tonefile = wave.open('pure_tone3.wav', 'w')

# set parameters for pure tone
tonefile.setframerate(SAMPLERATE)
tonefile.setnchannels(NCHANNELS)
tonefile.setsampwidth(2) # 8 bits per byte = 16bit

# get buffers
tonebuffer = tone.get_raw()

# write raw buffer to the wave file
tonefile.writeframesraw(tonebuffer)

# neatly close the wave file objects
tonefile.close()
