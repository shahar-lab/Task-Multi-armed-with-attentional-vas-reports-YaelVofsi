

import psychopy
from psychopy import core, visual, gui, data, visual, event
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random
from psychopy.visual.slider import Slider
import pygame
from random import sample
import random


################################################################################################################
####set experiment configuration --------------

# number of trials and blocks
Ntrials          = 3
Nblocks          = 2

#timing in the trial
trial_timing =  {
  "ITI": [1],
  "choice_feedback": [0.5],
  "outcome": [1]
}


#reward probabilities
arms_prob   =[0.35,0.45,0.55,0.65]


#change to True/False to include section in the next run
instructionsPhase = False
quizPhase         = False
trainPhase        = False
gamePhase         = True
############################################################################################################







#### Make a text file to save data ---------------------------------------
expInfo  = {"subject": "0"}
dlg      = gui.DlgFromDict(expInfo, title="Yael's Flowers Task")
fileName = "flowers_task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, thought probe, trial, chosen, unchosen, offer_right_image, offer_left_image, exp_value_right, exp_value_left, choice_location, choice_key, exp_value1, exp_value2, exp_value3, exp_value4, RT, reward, vas, RT_vas, coins_per_block, coins_per_task, ntrial_to_prob, count_to_prob\n")
subjectN = expInfo["subject"]


####initializing game -----------------------------------------
#xbox controller
pygame.init()
clock       = pygame.time.Clock()
keepPlaying = True
j           = pygame.joystick.Joystick(0)
j.init()

# create a window
win     = visual.Window( [1920, 1080], fullscr = True, monitor="testMonitor", units="deg", color=(1, 1, 1), useFBO=False)
win.mouseVisible = False
mytimer = core.Clock()



####set stimuli--------------
won        = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost       = visual.ImageStim(win, image="ur.png", pos=[0, 0], size=4)
fixation   = visual.TextStim(win, text="+", pos=[0, 0], color=(-1, -1, -1))
hourglass  = visual.ImageStim(win, image="hourglass.png", pos=[0,0], size=4)
left_rect  = visual.Rect(win, size = (6,7), lineColor=(-1, -1, -1), pos= [-6,0])
right_rect = visual.Rect(win, size = (6,7), lineColor=(-1, -1, -1), pos= [6,0])
question   = visual.TextStim(win, (':עגרכ הלטמל ילש בשקה תמר'),color=(-1, -1, -1), colorSpace='rgb',pos=(0,10))
pressA     = visual.TextStim(win, ('הריחבל A ץחל'),color=(-1, -1, -1), colorSpace='rgb',pos=(0,-10))
vas        = Slider(win,
             ticks=(1, 100),
             labels=('ללכ בשק אלל'  , 'אלמ בשק'),
             granularity=0,
             color='black',
             fillColor='black',
             borderColor='black',
             startValue=50, 
             labelHeight=None,
             size=(40,1.5))

#additional vars
coins_per_task  = 0 
coins_per_block = 0     
coordinates     =-9999

#### set counterbalance and images ------------------------
training_image_set = [ "practice_1.png", "practice_2.png", "practice_3.png", "practice_4.png" ]

picList = sample([ [ "1.png", "2.png", "3.png", "4.png" ],
                   [ "5.png", "6.png", "7.png", "8.png" ] ,
                   [ "9.png", "10.png", "11.png", "12.png" ] , 
                   [ "13.png", "14.png", "15.png", "16.png" ], 
                   [ "17.png", "18.png", "19.png", "20.png" ], 
                   ["21.png", "22.png", "23.png", "24.png" ], 
                   [ "25.png", "26.png", "27.png", "28.png" ], 
                   [ "29.png", "30.png", "31.png", "32.png"] ], Nblocks)


# experiment flow
def main():
    
    #these controll which section of the experiment are going to be displayed
    global instructionsPhase
    global quizPhase
    global trainPhase
    global gamePhase
    
#### Instructions -----------------------------
    if instructionsPhase:
        instructionsFunc()
        # Changing Phase to quiz Phase
        instructionsPhase = False
        quizPhase = True
        trainPhase = False
        gamePhase = False
    
#### Quiz -----------------------------
    if quizPhase:
        quizFunc()
        # Changing Phase to Training Phase
        instructionsPhase = False
        quizPhase = False
        trainPhase = True
        gamePhase = False

#### Training -----------------------------
    if trainPhase:
        
        current_block  = 0
        training_intro = visual.ImageStim(win, image="train1.png",  units='norm', size=[2,2], interpolate = True)
        stim1       = visual.ImageStim(win, image=training_image_set[0], pos=[-9, -5], size=(4,4))
        stim2       = visual.ImageStim(win, image=training_image_set[1], pos=[-3, -5], size=(4,4))
        stim3       = visual.ImageStim(win, image=training_image_set[2], pos=[+3, -5], size=(4,4))
        stim4       = visual.ImageStim(win, image=training_image_set[3], pos=[+9, -5], size=(4,4))
        training_intro.draw()
        stim1.draw()
        stim2.draw()
        stim3.draw()
        stim4.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
            
                    mainExperimentModes(dataFile, current_block, subjectN, win, "not presented", 6, 'test', training_image_set,trial_timing)
                    end_training = visual.ImageStim(win, image="end_training.png",  units='norm', size=[2,2], interpolate = True)
                    end_training.draw()
                    win.update()
                    # wait for response to end practice block
                    while True:
                        events = pygame.event.poll()
                        if (events.type == pygame.JOYBUTTONDOWN):
                            #Event 4 -> Pressing down left button
                            if events.button == 4:
                                break
                    # Changing Phase to Game Phase
                    instructionsPhase = False
                    quizPhase = False
                    trainPhase = False
                    gamePhase = True
                    break
#### Test -----------------------------

    if gamePhase:
        outro = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)


        ####BLOCK LOOP--------------------------------
        for current_block in range(Nblocks):
                print(current_block)
                
                #set stim images for current block
                currSet = picList[current_block]

                #block instructions screen
                startBlock  = "startBlock" + str(current_block+1) + ".png"
                endBlock    = "endBlock" + str(current_block+1) + ".png"
                start       = visual.ImageStim(win, image=startBlock,  units='norm', size=[2,2], interpolate = True)
                end         = visual.ImageStim(win, image=endBlock,  units='norm', size=[2,2], interpolate = True)
                stim1       = visual.ImageStim(win, image=currSet[0], pos=[-9, -5], size=(4,4))
                stim2       = visual.ImageStim(win, image=currSet[1], pos=[-3, -5], size=(4,4))
                stim3       = visual.ImageStim(win, image=currSet[2], pos=[+3, -5], size=(4,4))
                stim4       = visual.ImageStim(win, image=currSet[3], pos=[+9, -5], size=(4,4))
                start.draw()
                stim1.draw()
                stim2.draw()
                stim3.draw()
                stim4.draw()

                win.update()
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    # Wait for response to begin block
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:
                            ####MAIN TRIALS LOOP
                            mainExperimentModes(dataFile, current_block, subjectN, win, "not presented", Ntrials, 'test', currSet,trial_timing)
                            break
####end block feedback--------------
                #draw end block screen
                end.draw()
                coinsBox = visual.TextStim(win, text= str(coins_per_block), pos=[0,0], color=(0,0,0))
                coinsBox.draw()
                win.update()


                # wait for response to end block
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:
                            break
####end task feedback-----------------------
        blockend   = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)
        coinsBox   = visual.TextStim(win, text= str(coins_per_task), pos=[0,0], color=(0,0,0))
        blockend.draw()
        coinsBox.draw()

        win.update()
        while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressed left Button
                        if events.button == 4:
                            break



# # # # # # #
# Functions #
# # # # # # #

def abort(window):
    # check keyboard presses
    kb = keyboard.Keyboard()
    kb.start()
    keys = kb.getKeys(["escape"])
    if "escape" in keys:
        window.close()
        core.quit()

def WrongAnswerFunc():
    mistake = visual.ImageStim(win, image="mistake.png",  units='norm', size=[2,2], interpolate = True)    
    mistake.draw()
    win.update()
    while True:
        abort(win)
        events = pygame.event.poll()
        if (events.type == pygame.JOYBUTTONDOWN):
            # Pressed A for "Try Again"
            if (events.button == 0):
                break
            # Pressed B for "Go over instructions"
            elif (events.button == 1):
                instructionsFunc()
                break

def instructionsFunc():
    currSlide = 1
    while currSlide < 11:
        slideName = "slide" + str(currSlide) + ".png"
        slidePic = visual.ImageStim(win, image=slideName,  units='norm', size=[2,2], interpolate = True)
        slidePic.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    currSlide = currSlide + 1
                    break
                if (events.button == 5 and currSlide > 1) :
                    currSlide = currSlide - 1
                    break

def quizFunc():
    nTest = 1
    while nTest < 6:
        slideName = "quizQ" + str(nTest) + ".png"
        testPic = visual.ImageStim(win, image=slideName,  units='norm', size=[2,2], interpolate = True)
        testPic.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                # Question 1
                if nTest == 1:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 2 -> Pressed X Button
                    elif (events.button == 0) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1
                        break    
                
                # Question 2
                if nTest == 2:
                    # Correct Answer Case
                    # Event 0 -> Pressed A Button
                    if events.button == 0:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 1 -> Pressed B Button
                    # 
                    elif (events.button == 1) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break 
                
                # Question 3
                if nTest == 3:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 2 -> Pressed X Button
                    elif (events.button == 0) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 4
                if nTest == 4:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if (events.button == 1):
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    elif (events.button == 0):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 5
                if nTest == 5:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    elif (events.button == 0):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

def mainExperimentModes(dataFile, current_block, subjectN, win, cond, trials, blockType, currSet,trial_timing):
    
    ####first trial initial vars ----------------
    
    #amount of rewards
    global coins_per_block    
    global coins_per_task

    coins_per_block = 0
    coins_per_task+=coins_per_block

    #amount of trials to first thought probe
    ntrials_to_prob=random.randrange(2, 3)
    count_to_prob  =1




    ##### TRIAL LOOP -----------------------------------------

    for t in range(1, trials+1):
        mytimer = core.Clock()
        
        #### STIMULI--------------
        
        #fixation
        fixation.draw()
        win.update()
        core.wait(trial_timing['ITI'][0])

        #target
        offer = sample(range(4),2)
        stimL = visual.ImageStim(win, image=currSet[offer[0]], pos=[-6, 0], size=(6,6))
        stimR = visual.ImageStim(win, image=currSet[offer[1]], pos=[6, 0], size=(6,6))
        fixation.draw()
        stimL.draw()
        stimR.draw()
        win.update()
        mytimer.reset(0)
        
        ####RESPONSE ---------------------------------------
        while True:
            abort(win)
            
            #### RESPONSE TIMEOUT ----------------------------------------------------------------
            if (mytimer.getTime() > 6):
                # skip trial
                stimapr = "None"
                rt_warning = visual.TextStim(win, text= " רתוי רהמ ביגהל שי", pos=[0,0], color=(-1,-1,-1)) # יש להגיב מהר יותר
                rt_warning2 = visual.TextStim(win, text= "ךשמהל אוהשלכ שקמ לע ץוחלל שי", pos=[0,-10], color=(-1,-1,-1)) # יש ללחוץ על מקש כלשהוא להמשך
                rt_warning.draw()
                rt_warning2.draw()


                win.update()
                dataFile.write("%s, %s, %s, %s, %s, %s,"
                    % (
                        subjectN, 
                        blockType,
                        current_block, 
                        [],
                        t,
                        "NULL",
                    ))
                while True:
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                        # event 4 -> pressing down left button
                        if (events.button == 4 | events.button == 5):
                            break
                break
            events = pygame.event.poll()

            ##### COLLECT RESPONSE ------------------------------------------------------------------
            if (events.type == pygame.JOYBUTTONDOWN):
                
                #sub pressed LEFT
                if events.button == 4: 

                    RT = str(mytimer.getTime())

                    stimL.draw()

                    #save vars
                    prob_chosen     = arms_prob[offer[0]] # left flower prob 
                    prob_unchosen   = arms_prob[offer[1]]  # right flower prob
                    chosen          = offer[0]
                    unchosen        = offer[1]
                    key             = 1
                    stimapr         = "left"

                    break
                
                #sub pressed RIGHT
                elif events.button == 5: 
                    
                    RT = str(mytimer.getTime())

                    stimR.draw()
 
                    #save vars
                    prob_chosen     = arms_prob[offer[1]] # right flower prob 
                    prob_unchosen   = arms_prob[offer[0]] # left flower prob
                    chosen          = offer[1]
                    unchosen        = offer[0]
                    key             = 2
                    stimapr         = "right"
                    break           
    
                #choice feedback screen (choice was drawen above)
                fixation.draw()
                win.update()
                core.wait(trial_timing['choice_feedback'][0])
        
        #### OUTCOME -------------------------------------
        if (stimapr == "left"):
            stimL.draw()
        if (stimapr == "right"):
            stimR.draw()
        if (random.random() < prob_chosen):
            won.draw()
            coins_per_block+= 1
            coins_per_task += 1
            reward          = 1
        else:
            lost.draw()
            reward = 0
        win.update()
        core.wait(trial_timing['outcome'][0])
        

        #### THOUGHT PROBE-------------------------------------
        if (count_to_prob==ntrials_to_prob):   
            cond = 'probe'       
            vas.draw()
            question.draw()
            pressA.draw()
            win.flip()
            mytimer.reset(0)
            x=50
            while True:
                events = pygame.event.poll()
                #check joystick input
                # get joysticks axes
                x=x+j.get_axis(4)
                if (x>100): x=100
                if (x<1): x=1

                #print circles according to the joystick, adjusted with the screen size    
                vas.markerPos=(x)
                vas.draw()
                question.draw()
                pressA.draw()
                win.flip()

                #check to see if the button 'A' in the controller was pressed to stop the program    
                if(events.type == pygame.JOYBUTTONDOWN):
                    if(events.button == 0):
                        RT_vas = mytimer.getTime()
                        coordinates = x
                        vas.markerPos=(x)
                        question.draw()
                        pressA.draw()
                        vas.draw()
                        win.update()                       
                        core.wait(1)
                        
                        
                        break

        else:
            cond = 'no_probe'       
            coordinates    =-9999
            RT_vas = -9999
    
            


    
    #Save data --------------------------------------------------------------------------------------

        #save a line with choice-outcome data
        dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %f, %f, %f, %f, %f,%f\n" 
                        % (
                            subjectN,
                            blockType,
                            current_block+1,
                            cond,
                            t,
                            chosen+1,  
                            unchosen+1,
                            offer[0]+1,
                            offer[1]+1,
                            prob_chosen,
                            prob_unchosen,
                            stimapr, 
                            key,     
                            arms_prob[0],
                            arms_prob[1], 
                            arms_prob[2], 
                            arms_prob[3],
                            RT,
                            reward,
                            coordinates,
                            RT_vas,
                            coins_per_block,
                            coins_per_task,
                            count_to_prob,
                            ntrials_to_prob                            
                        )
                    )
        #save a thought probe trial
        if (count_to_prob == ntrials_to_prob): 
            
            #set the next amount of trials to probe
            ntrials_to_prob= random.randint(2, 3)
            count_to_prob  = 1
        else:
            count_to_prob +=1


main()

