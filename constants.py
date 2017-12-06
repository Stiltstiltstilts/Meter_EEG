#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import csv

FGC = (1, 1, 1) #white
BGC = (0, 0, 0) #grey
TEXTSIZE = 42 #text size for stim (not instructions)
TEXTCORDS = (0, 0) #Centre of screen
TRIALREPEATS = 1 # each trial last for approx 35seeconds 
beatFreq = 0.417 #2.4Hz
frameInterval = 0.0166667 #framerate.... CHECK THIS
soundDelay = 0.02 #CHECK THIS

#Instruction durations
condition_duration = 3 #duration for condition instructions prior to each trial
eye_duration = 2 #duration for prompt to close eyes

#####################
#####==STIMULI==#####
#####################

###===CONTROL===###
with open('WordList_Control.txt', 'r') as f: #open stimuli file as object
    reader = csv.reader(f, delimiter='\t')
    d = list(reader)

ControlWords = [] #create empty list for processed words
for n in range(0,len(d)):
    sen = d[n][0].split(' ') #going one line at a time spliting the sentence into seperate words
    ControlWords.append(sen)
###===BINARY===###
with open('WordList_Binary.txt', 'r') as f: #open stimuli file as object
    reader = csv.reader(f, delimiter='\t')
    d = list(reader)

BinaryWords = [] #create empty list for processed words
for n in range(0,len(d)):
    sen = d[n][0].split(' ') #going one line at a time spliting the sentence into seperate words
    BinaryWords.append(sen)
###===TERNARY===###
with open('WordList_Ternary.txt', 'r') as f: #open stimuli file as object
    reader = csv.reader(f, delimiter='\t')
    d = list(reader)

TernaryWords = [] #create empty list for processed words
for n in range(0,len(d)):
    sen = d[n][0].split(' ') #going one line at a time spliting the sentence into seperate words
    TernaryWords.append(sen)

BinaryPrompt = ['1', '2']
TernaryPrompt = ['1', '2', '3']



