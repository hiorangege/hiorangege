from psychopy import core, monitors, clock, visual, event
from psychopy.hardware import keyboard
import numpy as np
from time import localtime, strftime
import os
import matplotlib.pyplot as plt
import random
import pickle as pkl
from scipy import io

# part you want to change
subjID = 'CN001'
expType=1; #1表示进行MLM,  2表示进行MHM
timeStamp = strftime('%Y%m%d%H%M%S', localtime())
fileName = f'{timeStamp}_UG_{subjID}'
print(fileName)

alldata = {} # dict to save all data
alldata.update({'subjID': subjID})

triggerKey = 's'

time1=(1,2) #new partner dispT
time2=1 #blank screen 
time3=1  #offer dispT
time4=1 #iti

mon= monitors.Monitor('ECNUmri')  #使用某种屏幕预设？
mon.setDistance(90)  # View distance cm
mon.setSizePix([1024, 768]) #
mon.setWidth(37)  # cm
fps = 60 # monitor frame per seconds
refreshInterval = 1/fps
timeFactor = 0.17

win = visual.Window([1024, 768], units='deg', monitor=mon, checkTiming=True, colorSpace='rgb255',color=(101,101,101), allowGUI=False)

win.recordFrameIntervals = True # record frame intervals
win.waitBlanking=True # to return flip time
alldata.update({'fps':fps, 'refreshInterval':refreshInterval})

a=np.random.randn(20)*1.5+8
b=np.random.randn(20)*1.5+4
c=np.random.randn(20)*1.5+8
d=np.random.randn(20)*1.5+12
if expType==1:    
    offerlist=np.append(a,b)
    offerlist=np.append(offerlist,c)
else:
    offerlist=np.append(a,d)
    offerlist=np.append(offerlist,c)

rating_list=np.append(np.ones(36),np.zeros(24))
random.shuffle(rating_list)
alldata.update({'offerlist':offerlist,'rating_list':rating_list})

#-------------------
text_0 = visual.TextStim(win=win,text=f'Wait for trigger key {triggerKey}', height=1, units='deg',color='white')

text_1 = visual.TextStim(win, text =f'New partner is proposing',height = 1,pos = (0.0,0.2),color = 'white',units='deg')
text_2_1 = visual.TextStim(win, text =f'proposed split',height =1,pos = (0,6),color = 'white',units='deg')
text_2_2 = visual.TextStim(win, text =f'partner',height =1,pos = (-4,2),color = 'white',units='deg')
text_2_3 = visual.TextStim(win, text =f'you',height =1,pos = (4,2),color = 'white',units='deg')
text_2_4 = visual.TextStim(win, text =f'',height =1,pos = (-4,0),color = 'white',units='deg')
text_2_5 = visual.TextStim(win, text =f'',height =1,pos = (4,0),color = 'white',units='deg')

option_vert = [[1.5,0.7],[-1.5,0.7],[-1.5,-0.7],[1.5,-0.7]]
option_accept=visual.ShapeStim(win, fillColor=(50,50,50),colorSpace='rgb255',vertices = option_vert,pos=(-3,-3))
option_reject=visual.ShapeStim(win, fillColor=(50,50,50),colorSpace='rgb255',vertices = option_vert,pos=(3,-3))
text_accept = visual.TextStim(win, text =f'accept',height =1,pos = (-3,-3),color = 'white',units='deg')
text_reject = visual.TextStim(win, text =f'reject',height =1,pos = (3,-3),color = 'white',units='deg')

text_4_1 = visual.TextStim(win, text =f'How do you feel about the proposal',height =1,pos = (0,4),color = 'white',units='deg')

card_vert = [[0.5,0.5],[-0.5,0.5],[-0.5,-0.5],[0.5,-0.5]]
card=[];
for i in range(9):
    card.append(visual.ShapeStim(win, fillColor=(50,50,50),colorSpace='rgb255',vertices = card_vert))
    card[i].pos=((i-4)*1.5,0)
num_text= visual.TextStim(win,height =1,color = 'white',units='deg')
mymouse=event.Mouse(visible=True)

card_vert = [[0.5,0.5],[-0.5,0.5],[-0.5,-0.5],[0.5,-0.5]]
card_1 = visual.ShapeStim(win, fillColor=(50,50,50),colorSpace='rgb255',vertices = card_vert)

event.globalKeys.clear()
event.globalKeys.add(key='q', func=core.quit)  # global quit key
timer = core.Clock()

#------------------------------
text_0.draw()
win.flip()
event.waitKeys(keyList=[triggerKey])
win.flip()
core.wait(2-refreshInterval*timeFactor)

subres1=[];
RT1=[];
subres2=[];
RT2=[];

for trial in range(len(offerlist)):
    print(trial)
    text_1.draw()
    win.flip()
    core.wait(np.random.rand()*(time1[1]-time1[0])+time1[0])
    win.flip()
    core.wait(time2-refreshInterval*timeFactor)

    text_2_1.draw()
    text_2_2.draw()
    text_2_3.draw()
    text_2_4.text=f'{20-np.round(offerlist[trial],1)}'  #对家
    text_2_5.text=f'{np.round(offerlist[trial],1)}'   #被试
    text_2_4.draw()
    text_2_5.draw()
    win.flip()
    core.wait(time3-refreshInterval*timeFactor)

    text_2_1.draw()
    text_2_2.draw()
    text_2_3.draw()
    text_2_4.draw()
    text_2_5.draw()
    option_accept.draw()
    option_reject.draw()
    text_accept.draw()
    text_reject.draw()
    win.flip()
    timer.reset()
    subres=0
    while 1:
        if mymouse.isPressedIn(option_accept,buttons=[0]):
                subres=1
                RT=timer.getTime()
                break
        elif mymouse.isPressedIn(option_reject,buttons=[0]):
                subres=2
                RT=timer.getTime()
                break
    subres1.append(subres)
    RT1.append(RT)
    
    if rating_list[trial]==1:
        win.flip()
        core.wait(time2-refreshInterval*timeFactor)
        text_4_1.draw()
        for i in range(9):
            card[i].draw()
            num_text.text=f'{i+1}'
            num_text.pos = ((i-4)*1.5,0)
            num_text.draw()
        win.flip()
        timer.reset()
        subres=0;
        while 1:
            for i in range(9):
                if mymouse.isPressedIn(card[i],buttons=[0]):
                    subres=i+1
                    RT=timer.getTime()
                    break
            if subres!=0:
                break
        subres2.append(subres)
        RT2.append(RT)        
    win.flip()
    core.wait(time4-refreshInterval*timeFactor)

alldata.update({'subres1':subres1,'RT1':RT1,'subres2':subres2,'RT2':RT2})
win.close()

with open(f'{fileName}.pkl', 'wb') as f:
    pkl.dump(alldata, f)

io.savemat(f'{fileName}.mat', {'alldata': alldata})

