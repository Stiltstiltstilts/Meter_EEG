#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#from __future__ import division

from psychopy import core, visual, logging, gui, event, parallel, prefs
import sounddevice as sd
import soundfile as sf
prefs.general['audioLib'] = ['sounddevice']
from psychopy import sound
from numpy.random import random, randint, normal, shuffle
import os, sys, itertools  
from constants import *

GlobalClock = core.Clock() # Track time since experiment starts

#port = parallel.ParallelPort(address=0xd050)
#port.setData(0)

# Ensures that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session (from prompt box)
expName = 'Exp1'  
expInfo = {u'session': u'001', u'participant': u'', u'order':1}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
#expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name
filename = _thisDir + os.sep + u'data/%s_%s' % (expName, expInfo['participant'])


# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file


# ====================== #
# ===== VARIABLES ====== #
# ====================== #
####====Auditory Stimuli====####
beat_stim, samplerate = sf.read(u'beat_stim.wav')
sd.default.samplerate = samplerate
#beat_stim = sound.Sound(u'beat_stim.wav') 
#beat_stim.setVolume(1) #Beat stimulus

win = visual.Window(fullscr=False,
                monitor='Laptop',
                units='deg',
                allowGUI=False)
                
"""
####====VISUAL STIMULI====####
colour_binary = visual.ImageStim(
    win=win, image=u'Stimuli/Col_2.png', mask=None,
    ori=0, pos=(0, 0), size=(4, 4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    interpolate=True, depth=0.0)
colour_ternary = visual.ImageStim(
    win=win, image=u'Stimuli/Col_3.png', mask=None,
    ori=0, pos=(0, 0), size=(4, 4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    interpolate=True, depth=0.0)
gesture_binary = visual.ImageStim(
    win=win, image=u'Stimuli/Gest_2.png', mask=None,
    ori=0, pos=(0, 0), size=(4, 4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    interpolate=True, depth=0.0)
gesture_ternary = visual.ImageStim(
    win=win, image=u'Stimuli/Gest_3.png', mask=None,
    ori=0, pos=(0, 0), size=(4, 4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    interpolate=True, depth=0.0)
"""

# ================================================= #
# =========== EXPERIMENTAL INSTRUCTIONS =========== #
# ================================================= #

bottomInst = ["Press space to continue.",
    "Press space to continue or backspace to go back.",
    "WHEN YOU'RE READY TO BEGIN, press space."]

topControl = ["Welcome to our study--thank you for participating!",
    "Today, you will be listening to a repetitive beat quite a bit.",
    "Think of it as a weird and wonderful form of meditation--for science!",
    "In this first section, you will listen to this beat while seeing words appear on the screen",
    "While this happens, you will have two tasks: a word task and a beat task.",
    "The word task is to identify if one of the words is a type of fish, like 'salmon'.",
    "The words appear only briefly, so you'll have to pay attention.",
    "The beat task is to identify whether the beat suddenly glitches/speeds up, press space to hear what this sounds like",
    "sound", #this triggers a sound file to be played as an example
    "At the end of each trial, the computer will ask whether there was a 'salmon' or a 'glitched beat'.",
    "As soon as you respond, the next trial will start automatically.",
    "Before each trial starts, a black cross appears at the centre of the screen.",
    "It is important that you keep your eyes fixated on this cross during the trial and to not move your eyes around.",
    "You can stretch and move your eyes in between trials, but not during them.",
    "During each trial, try and keep your body as still and relaxed as possible.",
    "So don't tap your foot, move your face, tongue, or even wiggle your toes in time with the beat",
    "If you have any questions or if anything wasn't clear, let the experimenter know now."]

topImagery = ["In this section of the experiment, your task is to imagine a specfic metrical interpretation of the beat.",
    "For example, ",
    "Specifically, you are to imagine the colours RED then BLUE in either groups of 2 or 3, changing colours in time with the beeps.",
    "For a group of two RED BLUE RED BLUE RED BLUE etc.",
    "And for a group of three RED BLUE BLUE RED BLUE BLUE etc.",
    "You will be told which of these patterns to imagine before the sound starts.",
    "Start this imagery from the first beep and maintain it all the way through as vividly as you can.",
    "You will also be asked to close your eyes during the sound. Open them again once the sound stops.",
    "Let the experimenter know if you have questions before continuing."]

topWords = ["Part 2",
    "This time, you will hear the same beat but there will be no interruptions.",
    "Your task is to use visual mental imagery to help you feel the beat in either 2 or 3 beat patterns",
    "Specifically, you are to imagine the colours RED then BLUE in either groups of 2 or 3, changing colours in time with the beeps.",
    "For a group of two RED BLUE RED BLUE RED BLUE etc.",
    "And for a group of three RED BLUE BLUE RED BLUE BLUE etc.",
    "You will be told which of these patterns to imagine before the sound starts.",
    "Start this imagery from the first beep and maintain it all the way through as vividly as you can.",
    "You will also be asked to close your eyes during the sound. Open them again once the sound stops.",
    "Let the experimenter know if you have questions before continuing."]

topGesture = ["Part 3",
    "This time your task is to imagine UP and DOWN gestures in time with the beeps",
    "Like before, these will come in either groups of 2 or 3 and you will be told which before each test.",
    "The experimenter will come in and demonstrate what this means.",
    "Like before, you will also be asked to close your eyes during the sound. And opening them again once the sound stops.",
    "Let the experimenter know if you have questions before continuing."]

# ==================================== #
# ===== TRIAL LIST CONSTRUCTION ====== #
# ==================================== #

controlTrials = []
for x in range(TRIALREPEATS):
    b = ControlWords[:] #make copy of list to enable shuffling
    shuffle(b)
    c = list(itertools.chain(*b))
    trial = {'prompt':c, 'sound':beat_stim, 'ref':1} # 'ref' is for the EEG triggers
    controlTrials.extend([trial])

word2Trials = []
for x in range(TRIALREPEATS):
    b = BinaryWords[:]
    shuffle(b)
    c = list(itertools.chain(*b))
    trial = {'prompt':c, 'sound':beat_stim, 'ref':2}
    word2Trials.extend([trial])

word3Trials = []
for x in range(TRIALREPEATS):
    b = TernaryWords[:]
    shuffle(b)
    c = list(itertools.chain(*b))
    trial = {'prompt':c, 'sound':beat_stim, 'ref':3}
    word3Trials.extend([trial])

imagery2Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(BinaryPrompt * 40), 'sound':beat_stim, 'ref':4}
    imagery2Trials.extend([trial])

imagery3Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(TernaryPrompt * 30), 'sound':beat_stim, 'ref':5}
    imagery3Trials.extend([trial])

gest2Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(BinaryPrompt * 40), 'sound':beat_stim, 'ref':6}
    gest2Trials.extend([trial])

gest3Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(TernaryPrompt * 30), 'sound':beat_stim, 'ref':7}
    gest3Trials.extend([trial])

allBlocks = []
if  expInfo['order'] == 1: #implementing counterbalancing order in trials
    allBlocks = [{'instructions':topWords, 'trials': [word2Trials] + [word3Trials]}] + [{'instructions':topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] + [{'instructions':topGesture, 'trials':[gest2Trials] + [gest3Trials]}] #ABC
elif expInfo['order'] == 2:
    allBlocks = [{'instructions': topWords, 'trials': [word2Trials] + [word3Trials]}] + [{'instructions': topGesture, 'trials': [gest2Trials] + [gest3Trials]}] + [{'instructions': topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] #ACB
elif expInfo['order'] == 3:
    allBlocks = [{'instructions': topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] + [{'instructions': topGesture, 'trials': [gest2Trials] + [gest3Trials]}] + [{'instructions':topWords, 'trials': [word2Trials] + [word3Trials]}] #BCA
elif expInfo['order'] == 4:
    allBlocks = [{'instructions':topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] + [{'instructions':topWords, 'trials': [word2Trials] + [word3Trials]}] + [{'instructions':topGesture, 'trials': [gest2Trials] + [gest3Trials]}] #BAC
elif expInfo['order'] == 5:
    allBlocks = [{'instructions':topGesture, 'trials': [gest2Trials] + [gest3Trials]}] + [{'instructions':topWords, 'trials': [word2Trials] + [word3Trials]}] + [{'instructions':topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] #CAB
elif expInfo['order'] == 6:
    allBlocks = [{'instruction':topGesture, 'trials': [gest2Trials] + [gest3Trials]}] + [{'instructions':topImagery, 'trials': [imagery2Trials] + [imagery3Trials]}] + [{'instructions':topWords, 'trials': [word2Trials] + [word3Trials]}] #CBA
#now flipping the order of binary and ternary  
elif expInfo['order'] == 7: 
    allBlocks = [{'instructions':topWords, 'trials': [word3Trials] + [word2Trials]}] + [{'instructions':topImagery, 'trials': [imagery3Trials] + [imagery2Trials]}] + [{'instructions':topGesture, 'trials': [gest3Trials] + [gest2Trials]}] #ABC 
elif expInfo['order'] == 8:
    allBlocks = [{'instructions':topWords, 'trials': [word3Trials] + [word2Trials]}] + [{'instructions':topGesture, 'trials': [gest3Trials] + [gest2Trials]}] + [{'instructions':topImagery, 'trials':[imagery3Trials] + [imagery2Trials]}] #ACB
elif expInfo['order'] == 9:
    allBlocks = [{'instructions':topImagery, 'trials':[imagery3Trials] + [imagery2Trials]}] + [{'instructions':topGesture, 'trials':[gest3Trials] + [gest2Trials]}] + [{'instructions':topWords, 'trials':[word3Trials] + [word2Trials]}] #BCA
elif expInfo['order'] == 10:
    allBlocks = [{'instructions': topImagery, 'trials':[imagery3Trials] + [imagery2Trials]}] + [{'instructions':topWords, 'trials':[word3Trials] + [word2Trials]}] + [{'instructions':topGesture, 'trials':[gest3Trials] + [gest2Trials]}] #BAC
elif expInfo['order'] == 11:
    allBlocks = [{'instructions':topGesture, 'trials':[gest3Trials] + [gest2Trials]}] + [{'instructions':topWords, 'trials':[word3Trials] + [word2Trials]}] + [{'instructions':topImagery, 'trials':[imagery3Trials] + [imagery2Trials]}] #CAB
elif expInfo['order'] == 12:
    allBlocks = [{'instructions':topGesture, 'trials':[gest3Trials] + [gest2Trials]}] + [{'instructions':topImagery, 'trials':[imagery3Trials] + [imagery2Trials]}] + [{'instructions':topWords, 'trials':[word3Trials] + [word2Trials]}] #CBA  



# ====================== #
# ===== START EXP ====== #
# ====================== #

try: 
    #Set up variables
    message1 = visual.TextStim(win, pos=[0,+3], color='#000000', alignHoriz='center', name='topMsg', text="placeholder") 
    message2 = visual.TextStim(win, pos=[0,-3], color='#000000', alignHoriz='center', name='bottomMsg', text="placeholder") 
    ratingCont = visual.RatingScale(win=win, name='ratingCont', marker=u'triangle', size=1.0, pos=[0.0, -0.4], choices=[u'No', u'Yes'], tickHeight=-1) #Rating for interruption control condition
    ratingCont_question = visual.TextStim(win, pos=[0,+3], color='#000000', alignHoriz='center', text="Was there a salmon or interruption?")
    fixation = visual.TextStim(win,  pos=[0,0], color='#000000', alignHoriz='center', text="+")
    circle = visual.TextStim(win,  pos=[0,0], color='#000000', alignHoriz='center', text="+")
    endMessage = visual.TextStim(win,  pos=[0,0], color='#000000', alignHoriz='center', text="The end!")
    ratingImag = visual.RatingScale(win=win, name='ratingCol', marker=u'triangle', size=1.0, pos=[0.0, -0.4], low=1, high=7, labels=[u'no image at all', u'fairly vivid', u'vivid as actual'], scale=u'') #Mental imagery rating
    ratingImag_question = visual.TextStim(win, pos=[0,+3], color='#000000', alignHoriz='center', text="How vivid was your mental imagery?")
    wordStim = visual.TextStim(win=win, pos=[0,0], color=FGC, text="placeholder")
    spaceCont = visual.TextStim(win=win, pos=[0,0], color=FGC, text="Press space to continue")
    clock = core.Clock()

   
    # ========================== #
    # ===== CONTROL BLOCK ====== #
    # ========================== #
    # ===== INSTRUCTIONS ====== #
    counter = 0
    while counter < len(topControl):
        if topControl[counter] == "sound":
            sd.play(beat_stim)
            core.wait(5)
            sd.stop()
        else:
            message1.setText(topControl[counter])
            if counter == 0:
                message2.setText(bottomInst[0])
            elif counter in range(1, (len(topControl) - 1)):
                message2.setText(bottomInst[1])
            else: 
                message2.setText(bottomInst[2])
        #display instructions and wait
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        #check for a keypress
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace':
            counter -= 1
        else:
            counter += 1

    # ===== TRIALS ====== #
    for trial in controlTrials:
        fixation.draw()
        win.flip() 
        core.wait(2) # Wait 2 seconds
        trial['sound'].play()
        #port.setData(trial['ref']) #Stim starts
        #core.wait(0.002)
        #port.setData(0)
        core.wait(soundDelay)
        clock.reset()
        for x in range(1, 80): # 79 beats/words
            wordStim.setText(trial['prompt'][(x-1)])
            wordStim.draw()
            win.flip() #lock clock timing to win.flip for frame 0
            while clock.getTime() < (beatFreq * x) - (frameInterval * 0.9): pass # until just before next frame of next beat
        trial['sound'].stop()
        win.flip() #clear
        while ratingCont.noResponse:
            ratingCont.draw()
            ratingCont_question.draw()
            win.flip()
        InterDetec = ratingCont.getRating()
        ratingCont.reset()
        core.wait(1)

    # ============================ #
    # ===== MAIN EXPERIMENT ====== #
    # ============================ #
    for blocks in allBlocks:
        # ===== INSTRUCTIONS ====== #
        counter = 0
        while counter < len(blocks['instructions']):
            message1.setText(blocks['instructions'][counter])
            if counter == 0:
                message2.setText(bottomInst[0])
            elif counter in range(1, (len(blocks['instructions']) - 1)):
                message2.setText(bottomInst[1])
            else: 
                message2.setText(bottomInst[2])
            #display instructions and wait
            message1.draw()
            message2.draw() 
            win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
            win.flip()
            #check for a keypress
            thisKey = event.waitKeys()
            if thisKey[0] in ['q','escape']:
                core.quit()
            elif thisKey[0] == 'backspace':
                counter -= 1
            else:
                counter += 1

        # ===== TRIALS ====== #
        for conditions in blocks['trials']:
            for trials in conditions:
                fixation.draw()
                win.flip() 
                core.wait(2) # Wait 2 seconds
                trials['sound'].play()
                #port.setData(trial['ref']) #Stim starts
                #core.wait(0.002)
                #port.setData(0)
                core.wait(soundDelay)
                clock.reset()
                for x in range(1, 80): # 79 beats/words
                    wordStim.setText(trials['prompt'][(x - 1)])
                    wordStim.draw()
                    win.flip() #lock clock timing to win.flip for frame 0
                    while clock.getTime() < (beatFreq * x) - (frameInterval * 0.9): pass # until just before next frame of next beat
                trials['sound'].stop()
                win.flip() #clear
                core.wait(2)
                #check for a keypress
                spaceCont.draw()
                win.flip()
                thisKey = event.waitKeys()
                if thisKey[0] in ['q','escape']:
                    core.quit()
                else:
                    win.flip()


finally:
    win.close()