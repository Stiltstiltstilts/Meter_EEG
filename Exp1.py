#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#from __future__ import division
from psychopy import core, visual, logging, gui, event, parallel, prefs, data
import sounddevice as sd
import soundfile as sf
prefs.general['audioLib'] = ['sounddevice']
from numpy.random import random, randint, normal, shuffle
from psychopy import sound
import os, sys, itertools  
from constants import *

#sd.default.device = 12 # Audigy ASIO driver for 16bit 48000HZ
#sd.default.latency = ('low','low')

GlobalClock = core.Clock() # Track time since experiment starts

#port = parallel.ParallelPort(address=0xd050) 
#port.setData(0)

# Ensures that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session (from prompt box)
expName = 'Beat_EEG'  
expInfo = {u'session': u'001', u'participant': u'', u'order':1, u'handedness':u'', u'headcirc':u'',u'gender':u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
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
beat_stim, sd.default.samplerate = sf.read(u'pure_tone3.wav')
beat_inter, sd.default.samplerate = sf.read(u'tone_interruption.wav')

win = visual.Window(fullscr=True,
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
    "When you're ready to begin, press space. Or press backspace to go back."]

topControl = ["Welcome to our study--thank you for participating!",
    "Today, you will be listening to an auditory beat quite a bit. Think of it as a weird and wonderful form of meditation--for science!",
    "In this first section, you will listen to this beat while seeing words flash on the screen.",
    "While this happens, you will have two tasks: a word task and a beat task.",
    "The word task is to identify if one of the words is a type of fish, like 'salmon'.",
    "The words appear only briefly, so you'll have to pay attention.",
    "The beat task is to identify whether the beat suddenly glitches/speeds up, press space to hear an example of what this sounds like.",
    "sound", #this triggers a sound file to be played as an example
    "At the end of each trial, the computer will ask whether there was a 'fish-word' or a 'glitched beat'.",
    "As soon as you respond, the next trial will start automatically. So don't confirm your answer until you are ready to continue. Feel free to take short breaks.",
    "Before each trial starts, a black cross appears at the centre of the screen.",
    "It is important that you keep your eyes fixated on this cross during the trial and to not move your eyes around.",
    "You can stretch and move your eyes in between trials, but not during them. Excessive eye movement can interfere with our recording of your brainwaves.",
    "During each trial, try and keep your body as still and relaxed as possible.",
    "So don't tap your foot, move your face, tongue, or even wiggle your toes in time with the beat.",
    "Also, do not actually pronounce the words you see with your mouth. Regular movements of the mouth/tongue can also interfer with our recording of your brainwaves.",
    "If anything is unclear, let the experimenter know and they can clarify. It is important that you feel comfortable in your understanding of the task.",
    ""]

topImagery = ["In this section of the experiment, your task is to imagine specfic metrical interpretations of the beat.",
    "While the beat we play you will always be the same, your task is to imagine it grouped in 2s (binary) or 3s (ternary).",
    "In music theory, this is know as meter. Binary is like 2/4 time, as in march music, and ternary is like 3/4 time, as in waltz music.",
    "image1", # this triggers an image file to help explain meter imagery
    "Before each trial, the computer will tell you to whether to imagine a 'binary' or a 'ternary' meter.",
    "Imagine the meter in a way that feels natural to you: how do you normally 'feel' the meter when you play or listen to music?",
    "The numbers '1 2' (binary) and '1 2 3' (ternary) will flash on the screen to guide you during the trial, where the '1' is the strong beat.",
    "Like before, however, be sure not to actually pronounce these numbers with your mouth, as these facial movements can interfere with our recording.",
    "Press spacebar to play a short excerpt of the experiment beat sound. Practise imagining binary or ternary meter to check you understand the task.",
    "sound",
    "If anything is unclear, let the experimenter know and they can clarify. It is important that you feel comfortable in your understanding of the task.",
    ""]

topWords = ["In this section of the experiment, words will flash on the screen in time with the beat.",
    "Your task is to silently read these words as they appear, like you would silently read a book.",
    "However, it is important that you DO NOT move your mouth and tongue while you read these words, as this can interfere with the recording of your brainwaves.",
    "So, keep your body and mouth relaxed during the task.",
    "Besides reading these words as they appear, your other task is to identify whether the trial you just listened to contained the phrase 'old swans'.",
    "During a trial, if you see this phrase, make a mental note of it while continuing to read the subsequent words. Then indicate 'yes I saw the phrase' at the end of the trial.",
    "If anything is unclear, let the experimenter know and they can clarify. It is important that you feel comfortable in your understanding of the task.",
    ""]

topGesture = ["In this section of the experiment, you will listen to the beat while imagining movement gestures (similar to conducting).",
    "Each beat you hear is to be imagined as a movement in space."
    "To make this more concrete, imagine you are chopping some wood with an axe. To swing the axe, you have the pull the axe back behind your head (UP) and then swing it at the wood (DOWN).",
    "This sequence of movements, UP (axe back) leading to DOWN (axe down), is what you need to imagine as vividly as you can, in time with the beats."
    "If it helps, actually imagine yourself chopping wood and try and feel the detailed sensations like the weight of the axe rushing down onto the wood, and the muscular effort required to swing.",
    "It is also important that the UP movement is not just the feeling of going upward, but it is the preparation that leads to the DOWN (you can't swing an axe if you don't first go 'UP')",
    "In this sense, you are always aiming for 'DOWN', and in order to get there you have to first go 'UP'.",
    "In this section, you will have to imagine either binary or ternary versions of this movement gesture.",
    "The binary version is the one just described: an alternation of UP -> DOWN, UP -> DOWN, UP -> DOWN etc.",
    "The ternary version is slightly different: an alternation of UP -> UP -> DOWN, UP -> UP -> DOWN, UP -> UP -> DOWN etc.",
    "Going back to the wood-chopping analogy, the extra 'UP' in the ternary version is like you not getting the axe high enough on the first 'UP', so you have to make two 'UP' movements before finally swinging 'DOWN'.",
    "Press spacebar to hear the beat, and practice imagining these movements in time to the beat. Repeat sound as many times as you want by simply pressing backspace and space again once the sound stops.",
    "sound",
    "You will be told to imagine either 'binary' (UP -> DOWN) or 'ternary' (UP -> UP -> DOWN) at the start of each trial. And the words 'UP' and 'DOWN' will appear in time with the beat to guide you.",
    "As before, while you are imagining movements, it is important that you keep your body still and relaxed during the trial. As movements can interfere with brainwave recording.",
    "If anything is unclear, let the experimenter know and they can clarify. It is important that you feel comfortable in your understanding of the task.",
    ""]

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
 # add catch trial
catch = ControlWords[:]
catch2 = list(itertools.chain(*catch))
catch2 = catch2[:77]
catch2.extend(['tuna'])
shuffle(catch2)
temp = {'prompt':catch2, 'sound':beat_stim, 'ref':2}
controlTrials.extend([temp])
shuffle(controlTrials)
print controlTrials
word2Trials = []
for x in range(TRIALREPEATS):
    b = BinaryWords[:]
    shuffle(b)
    c = list(itertools.chain(*b))
    trial = {'prompt':c, 'sound':beat_stim, 'ref':3}
    word2Trials.extend([trial])

word3Trials = []
for x in range(TRIALREPEATS):
    b = TernaryWords[:]
    shuffle(b)
    c = list(itertools.chain(*b))
    trial = {'prompt':c, 'sound':beat_stim, 'ref':4}
    word3Trials.extend([trial])

imagery2Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(BinaryPrompt * 40), 'sound':beat_stim, 'ref':5, 'intro':u'Binary'}
    imagery2Trials.extend([trial])

imagery3Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(TernaryPrompt * 30), 'sound':beat_stim, 'ref':6, 'intro':u'Ternary'}
    imagery3Trials.extend([trial])

gest2Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(BinGestPrompt * 40), 'sound':beat_stim, 'ref':7, 'intro':u'Binary (UP -> DOWN)'}
    gest2Trials.extend([trial])

gest3Trials = []
for x in range(TRIALREPEATS):
    trial = {'prompt':(TernGestPrompt * 30), 'sound':beat_stim, 'ref':8, 'intro':u'Ternary (UP -> UP -> DOWN)'}
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


"""
# ====================== #
# ===== START EXP ====== #
# ====================== #

try: 
    #Set up variables
    message1 = visual.TextStim(win, pos=[0,+3], color=FGC, alignHoriz='center', name='topMsg', text="placeholder") 
    message2 = visual.TextStim(win, pos=[0,-3], color=FGC, alignHoriz='center', name='bottomMsg', text="placeholder") 
    ratingCont = visual.RatingScale(win=win, name='ratingCont', marker=u'triangle', size=1.0, pos=[0.0, -0.4], choices=[u'No', u'Yes'], tickHeight=-1) #Rating for interruption control condition
    ratingCont_question = visual.TextStim(win, pos=[0,+3], color=FGC, alignHoriz='center', text="Was there a salmon or interruption?")
    fixation = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="+")
    endMessage = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="The end!")
    wordStim = visual.TextStim(win=win, pos=[0,0], color=FGC, text="placeholder")
    spaceCont = visual.TextStim(win=win, pos=[0,0], color=FGC, text="Press space to continue")
    introText = visual.TextStim(win=win, pos=[0,0], color=FGC, text="Placeholder")
    meterImage = visual.ImageStim(win=win, image=u'imagery.jpg', pos=[0,+3], mask=None, size=(6,6))
    clock = core.Clock()



    # ========================== #
    # ===== CONTROL BLOCK ====== #
    # ========================== #
    # ===== INSTRUCTIONS ====== #
    counter = 0
    while counter < len(topControl):
        if topControl[counter] == "sound":
            sd.play(beat_inter)
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
        sd.play(trial['sound']) #loading the file into memory to eliminate possible buffering latencies
        sd.stop()
        fixation.draw()
        win.flip() 
        core.wait(2) # Wait 2 seconds
        port.setData(trial['ref']) #~102ms before stim starts
        core.wait(0.002)
        port.setData(0)
        win.flip() # start of routine to compensate for sound latency
        clock.reset()
        sd.play(trial['sound'])
        while clock.getTime() < soundDelay - (frameInterval * 0.9): win.flip()  
        clock.reset()
        for x in range(1, 80): # 79 beats/words
            wordStim.setText(trial['prompt'][(x-1)])
            wordStim.draw()
            win.flip() #lock clock timing to win.flip for frame 0
            while clock.getTime() < (beatFreq * x) - (frameInterval * 0.9): pass # until just before next frame of next beat
        sd.stop()
        while ratingCont.noResponse:
            ratingCont.draw()
            ratingCont_question.draw()
            win.flip()
        InterDetec = ratingCont.getRating()
        ratingCont.reset()
        core.wait(0.5) 


    # ============================ #
    # ===== MAIN EXPERIMENT ====== #
    # ============================ #
    for blocks in allBlocks:
        # ===== INSTRUCTIONS ====== #
        counter = 0
        while counter < len(blocks['instructions']):
            if blocks['instructions'][counter] == "sound":
                sd.play(beat_stim)
                message2.setText(bottomInst[1])
                message2.draw()
                win.flip()
                core.wait(10)
                sd.stop()
            elif blocks['instructions'][counter] == "image1":
                meterImage.draw()
            else: 
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
                sd.play(trial['sound']) #loading the file into memory to eliminate possible buffering latencies
                sd.stop()
                if 'intro' in trials:
                    introText.setText(trials['intro'])
                    introText.draw()
                    win.flip()
                    core.wait(1)
                fixation.draw()
                win.flip() 
                core.wait(2) # Wait 2 seconds
                port.setData(trials['ref']) # ~105ms before stim starts
                core.wait(0.002)
                port.setData(0)
                win.flip() # start of routine to compensate for audio latency
                clock.reset()
                sd.play(trials['sound'])
                while clock.getTime() < soundDelay - (frameInterval * 0.9): win.flip()
                clock.reset()
                for x in range(1, 80): # 79 beats/words
                    wordStim.setText(trials['prompt'][(x - 1)])
                    wordStim.draw()
                    win.flip() #lock clock timing to win.flip for frame 0
                    while clock.getTime() < (beatFreq * x) - (frameInterval * 0.9): pass # until just before next frame of next beat
                sd.stop()
                win.flip() #clear
                #check for a keypress
                spaceCont.draw()
                win.flip()
                thisKey = event.waitKeys()
                if thisKey[0] in ['q','escape']:
                    core.quit()
                else:
                    win.flip()
    endMessage.draw()
    win.flip()
    core.wait(5)
    

finally:
    win.close()
"""