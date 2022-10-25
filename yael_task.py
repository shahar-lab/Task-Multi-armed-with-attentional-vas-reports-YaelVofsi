import psychopy
from psychopy import core, visual, gui, data, visual, event
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random
from psychopy.visual.slider import Slider

import pygame


# Make a text file to save data
expInfo = {"subject": "0"}
dlg = gui.DlgFromDict(expInfo, title="Yael's Flowers Task")
fileName = "flowers_task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, thought probe, trial, right_offer, left_offer, offer_right_image, offer_left_image, exp_value_right, exp_value_left, exp_value_chosen, choice_location, choice_key, choice_flower, unchosen_flower, chosen_flower_image, unchosen_flower_image, exp_value1, exp_value2, exp_value3, exp_value4, RT, reward, coins\n")
subjectN = expInfo["subject"]
# choice_key = 1 -> left, choice_key = 2 -> right
#initializing game
pygame.init()
clock = pygame.time.Clock()
keepPlaying = True
j = pygame.joystick.Joystick(0)
j.init()

# create a window
win = visual.Window( [1920, 1080], fullscr = True, monitor="testMonitor", units="deg", color=(1, 1, 1), useFBO=False)
win.mouseVisible = False
mytimer = core.Clock()

# number of trials and constant pictures
from random import sample
n = 5 # number of trials in each block
#stim_id = np.zeros(n)
total_coins=0 #global var
coins = 0     #global var
won = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost = visual.ImageStim(win, image="ur.png", pos=[0, 0], size=4)
fixation = visual.TextStim(win, text="+", pos=[0, 0], color=(-1, -1, -1))
hourglass = visual.ImageStim(win, image="hourglass.png", pos=[0,0], size=4)
left_rect = visual.Rect(win, size = (6,7), lineColor=(-1, -1, -1), pos= [-6,0])
right_rect = visual.Rect(win, size = (6,7), lineColor=(-1, -1, -1), pos= [6,0])
question = visual.TextStim(win, (':עגרכ הלטמל ילש בשקה תמר'),color=(-1, -1, -1), colorSpace='rgb',pos=(0,10))
pressA = visual.TextStim(win, ('הריחבל A ץחל'),color=(-1, -1, -1), colorSpace='rgb',pos=(0,-10))
vas = Slider(win,
             ticks=(1, 100),
             labels=('ללכ בשק אלל'  , 'אלמ בשק'),
             granularity=0,
             color='black',
             fillColor='black',
             borderColor='black',
             startValue=50, 
             labelHeight=None,
             size=(40,1.5))


# counterbalance, sets of pictures, and pictures of sets
subject_id = (int(subjectN))%2 # previously x
flower_set1 = [ "1.png", "2.png", "3.png", "4.png" ]
flower_set2 = [ "5.png", "6.png", "7.png", "8.png" ] 
flower_set3 = [ "9.png", "10.png", "11.png", "12.png" ] 
flower_set4 = [ "13.png", "14.png", "15.png", "16.png" ] 
flower_set5 = [ "17.png", "18.png", "19.png", "20.png" ] 
flower_set6 = [ "21.png", "22.png", "23.png", "24.png" ] 
flower_set7 = [ "25.png", "26.png", "27.png", "28.png" ] 
flower_set8 = [ "29.png", "30.png", "31.png", "32.png" ] 
deckList = [ [ "1.png", "2.png", "3.png", "4.png" ], [ "5.png", "6.png", "7.png", "8.png" ] , [ "9.png", "10.png", "11.png", "12.png" ] , [ "13.png", "14.png", "15.png", "16.png" ], [ "17.png", "18.png", "19.png", "20.png" ], ["21.png", "22.png", "23.png", "24.png" ], [ "25.png", "26.png", "27.png", "28.png" ], [ "29.png", "30.png", "31.png", "32.png"] ]
deck = [flower_set1, flower_set2, flower_set3, flower_set4, flower_set5, flower_set6, flower_set7, flower_set8]
picList = sample(deckList, 8)
print(picList)


# experiment flow
def main():
    instructionsPhase = False
    trainPhase = False
    quizPhase = False
    gamePhase = True
    
    # Start Instruction Phase
    if instructionsPhase:
        instructionsFunc()
        # Changing Phase to quiz Phase
        instructionsPhase = False
        quizPhase = True
        trainPhase = False
        gamePhase = False
    
    # Start Test\Quiz Phase
    if quizPhase:
        quizFunc()
        # Changing Phase to Training Phase
        instructionsPhase = False
        quizPhase = False
        trainPhase = True
        gamePhase = False

    # start training
    if trainPhase:
        blockCnt = 0
        training_intro = visual.ImageStim(win, image="train1.png",  units='norm', size=[2,2], interpolate = True)
        training_intro.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    #delayCond = "1 second"
                    mainExperimentModes(dataFile, blockCnt, subjectN, win, "not presented" , 5, 'practice', flower_set1) # practice without thought probe
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
    # start game:

    if gamePhase:
        outro = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)
        blockCnt = 0
        # Counterbalance block order
        blockOrder = [ [0]] #        blockOrder = [ [0,0,0,0,0,0,0,0]]

        # 0 -> delay 7 secs
        # 1 -> delay 1 second
        for x in blockOrder[subject_id]:
                blockCnt = blockCnt + 1
                currSet = picList[blockCnt-1]
                startBlock = "startBlock" + str(blockCnt) + ".png"
                endBlock = "endBlock" + str(blockCnt) + ".png"
                start = visual.ImageStim(win, image=startBlock,  units='norm', size=[2,2], interpolate = True)
                end = visual.ImageStim(win, image=endBlock,  units='norm', size=[2,2], interpolate = True)
                stim1 = visual.ImageStim(win, image=currSet[0], pos=[-9, -5], size=(4,4))
                stim2 = visual.ImageStim(win, image=currSet[1], pos=[-3, -5], size=(4,4))
                stim3 = visual.ImageStim(win, image=currSet[2], pos=[+3, -5], size=(4,4))
                stim4 = visual.ImageStim(win, image=currSet[3], pos=[+9, -5], size=(4,4))
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
                            mainExperimentModes(dataFile, blockCnt, subjectN, win, "not presented", n, 'test', currSet)
                            break
                #end block feedback
                end.draw()
                coinsBox = visual.TextStim(win, text= str(coins), pos=[0,0], color=(0,0,0))
                coinsBox.draw()
                win.update()
                global total_coins
                total_coins+=coins

                # Wait for response to end block
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:
                            break
        blockend   = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)
        coinsBox   = visual.TextStim(win, text= str(total_coins), pos=[0,0], color=(0,0,0))
        blockend.draw()
        coinsBox.draw()
        #win.update()
        #coinsBox = visual.TextStim(win, text= str(total_coins), pos=[0,0], color=(0,0,0))
        #coinsBox.draw()
        #outro.draw()
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

def mainExperimentModes(dataFile, blockCnt, subjectN, win, cond, trials, blockType, currSet):
    global coins
    coins = 0

    
    #delay_time = 0
    for i in range(1,5):
            if i==1:
                card_1=currSet[0]
            if i==2:
                card_2=currSet[1]
            if i==3:
                card_3=currSet[2]
            if i==4:
                card_4=currSet[3]
    probs = sample([0.35,0.35,0.65,0.65], 4)
    card_1_prob = probs[0]
    card_2_prob = probs[1]
    card_3_prob = probs[2]
    card_4_prob = probs[3]
    in_deck_card_order = []
    # Initilizing Game
    pygame.init()
    clock = pygame.time.Clock()
    j = pygame.joystick.Joystick(0)
    j.init()
    possibleOrder = [[0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1], [0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1]]
    block_id = blockCnt%2
    for t in range(1, trials+1):
        if (possibleOrder[block_id][t-1] == 1):
            cond = "presented"
        elif (possibleOrder[block_id][t-1] == 0):
            cond = "not presented"
        RTwarning = False
        mytimer = core.Clock()
        # Draw the stimuli and update the window
        presented = sample(currSet, 2)
        unpresented_cards=[]
        presented_probs = []
        for card in currSet:
            if card not in presented:
                unpresented_cards.append(card)
            else:
                # presented_probs.append(probs[int(card.split("_")[1])-1])
                if card == card_1:
                    in_deck_card_order.append("1")
                    presented_probs.append(card_1_prob)
                elif card == card_2:
                    in_deck_card_order.append("2")
                    presented_probs.append(card_2_prob)
                elif card == card_3:
                    in_deck_card_order.append("3")
                    presented_probs.append(card_3_prob)
                elif card == card_4:
                    in_deck_card_order.append("4")
                    presented_probs.append(card_4_prob)  
        stimL = visual.ImageStim(win, image=presented[0], pos=[-6, 0], size=(6,6))
        stimR = visual.ImageStim(win, image=presented[1], pos=[6, 0], size=(6,6))
        fixation.draw()
        win.update()
        core.wait(1)
        #draw stims
        fixation.draw()
        stimL.draw()
        stimR.draw()
        win.update()
        mytimer.reset(0)
        while True:
            abort(win)
            if (mytimer.getTime() > 6):
                # skip trial
                stimapr = "None"
                rt_warning = visual.TextStim(win, text= " רתוי רהמ ביגהל שי", pos=[0,0], color=(-1,-1,-1)) # יש להגיב מהר יותר
                rt_warning.draw()
                win.update()
                dataFile.write("%s, %s, %s, %s, %s, %s,"
                    % (
                        subjectN, 
                        blockType,
                        blockCnt, 
                        cond,
                        t,
                        "NULL",
                    ))
                while True:
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                        # event 4 -> pressing down left button
                        if (events.button == 4):
                            break
                break
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                # event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    RT = str(mytimer.getTime())
                    stimL.draw()
                    left_rect.draw()
                    fixation.draw()
                    win.update()
                    core.wait(0.5)
                    stim_id = (in_deck_card_order[0]) #left offer (chosen)
                    other_id = (in_deck_card_order[1]) #right offer
                    prob1 = presented_probs[1] # right flower prob 
                    prob2 = presented_probs[0] # left flower prob
                    curr_prob = prob2
                    key = 1
                    stimapr = "left"
                    dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," 
                        % (
                            subjectN,
                            blockType,
                            blockCnt,
                            cond,
                            t,
                            str(other_id),
                            str(stim_id),
                            presented[1],
                            presented[0],
                            prob1,
                            prob2,
                            prob2,
                            stimapr,
                            key,
                            str(stim_id),
                            str(other_id),
                            presented[0],
                            presented[1],
                            card_1_prob,
                            card_2_prob, 
                            card_3_prob, 
                            card_4_prob,
                            RT,
                        )
                    )
                    break
                elif events.button == 5:
                    RT = str(mytimer.getTime())
                    stimR.draw()
                    right_rect.draw()
                    fixation.draw()
                    win.update()
                    core.wait(0.5)
                    stim_id = (in_deck_card_order[1]) #right offer (chosen)
                    other_id = (in_deck_card_order[0]) #left offer
                    prob1 = presented_probs[1] # right flower prob 
                    prob2 = presented_probs[0] # left flower prob
                    curr_prob = prob1
                    key = 2
                    stimapr = "right"
                    
                    break           
    
        ##########################################
        # outcome using Random Walk for n trials #
        ##########################################
        if (stimapr == "left"):
            stimL.draw()
        if (stimapr == "right"):
            stimR.draw()
        if (random() < curr_prob):
            won.draw()
            coins = coins + 1
            reward = 1
            #dataFile.write("%i, %i,\n" % (1,coins,))
        else:
            lost.draw()
            reward = 0
            #dataFile.write("%i, %i,\n" % (0,coins,))
        win.update()
        core.wait(2)
        
        #### present thought probe-------------------------------------
        if (possibleOrder[block_id][t-1] == 1):          
            vas.draw()
            question.draw()
            pressA.draw()
            win.flip()
            x=50
            while True:
                events = pygame.event.poll()
                #check joystick input
                # get joysticks axes
                x=x+j.get_axis(4)
                if (x>100): x=100
                if (x<1): x=1
                #print circles according to the joystick, adjusted with the screen size    
                print(x)       
                vas.markerPos=(x)
                vas.draw()
                question.draw()
                pressA.draw()
                win.flip()
                #check to see if the button 'A' in the controller was pressed to stop the program    
                if(events.type == pygame.JOYBUTTONDOWN):
                    if(events.button == 0):
                        coordinates = x
                        vas.markerPos=(x)
                        question.draw()
                        pressA.draw()
                        vas.draw()
                        win.update()
                        #dataFile.write("%i,\n" % (coordinates,))
                        
                        core.wait(1)

                        break
    
    #Save data --------------------------------------------------------------------------------------
    dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s" 
                        % (
                            subjectN,
                            blockType,
                            blockCnt,
                            cond,
                            t,
                            str(stim_id),
                            str(other_id),
                            presented[1],
                            presented[0],
                            prob1,
                            prob2,
                            prob1,
                            stimapr,
                            key,
                            str(stim_id),
                            str(other_id),
                            presented[1],
                            presented[0],
                            card_1_prob,
                            card_2_prob, 
                            card_3_prob, 
                            card_4_prob,
                            RT,
                            reward,
                            #coordinates,
                            #coins,
                            #total_coins,
                        )
                    ) 
    dataFile.write("%i, %i,\n" % (0,coins,))      


                    
    




main()

