from psychopy import core, monitors, clock, visual, event
from psychopy.hardware import keyboard
import numpy as np
from time import localtime, strftime
import pickle as pkl
from os import rename
import matplotlib.pyplot as plt
from mriexpfun import setupeyelinkmri,closeupeyelinkmri 

# part you want to change
subjID = 'CN001'
runId = 1
timeFactor = 0.17 # 0~1, control timing, increase the value if you experience more delay.
wantEyeTrack = False  # whether need eyetracker


timeStamp = strftime('%Y%m%d%H%M%S', localtime())
fileName = f'{timeStamp}_faceprf_{subjID}_run{runId:02d}'  #format string, use{}  sign the var to be replaced
print(fileName)
mri = {} # dict to save all data
mri.update({'subjID': subjID, 'runId': runId, 'timeFactor':timeFactor})
#
triggerKey = 's'
mriFrameDur = 0.5
mri.update({'triggerKey': triggerKey, 'mriFrameDur': mriFrameDur})

# monitor stuff
mon= monitors.Monitor('ECNUmri')
mon.setDistance(90)  # View distance cm
mon.setSizePix([1024, 768])
mon.setWidth(37)  # cm
fps = 60 # monitor frame per seconds
refreshInterval = 1/fps
win = visual.Window([1024, 768], units='deg', monitor=mon, checkTiming=True, colorSpace='rgb255',color=(101,101,101), allowGUI=False)
win.recordFrameIntervals = True # record frame intervals
win.waitBlanking=True # to return flip time
mri.update({'fps':fps, 'refreshInterval':refreshInterval})
if wantEyeTrack:
    tmpEyeFile = timeStamp[:-8]+'.edf'
    try:
        tk = setupeyelinkmri(winsize=win.size, filename=tmpEyeFile)
    except:
        raise ConnectionError('Cannot link to Eyelink')
else:
    tk=None

# load stimulus and design
expDesign = np.load('faceprfdesign.npz')
images = expDesign['images']
posiCond = expDesign['posiCondList'][runId]
imageId = expDesign['imageIdList'][runId]
digitId = expDesign['digitList'][runId]
nMriFrame = imageId.size
mri.update({'posiCond': posiCond, 'imageId': imageId, 'digitId':digitId, 'nMriFrame':nMriFrame})

# stimulus stuff
fixSize = 0.3 # deg
faceSize  = 3.2 # deg, diameter
ecc = [-3.6, -1.8, 0, 1.8, 3.6]  # deg
allPosi =  [(i, j) for j in ecc for i in ecc]
mri.update({'fixSize':fixSize, 'faceSize': faceSize, 'ecc': ecc, 'allPosi': allPosi})

# ------------ experiment related stuff ----------------
# define
# create fixation and image object
fix = visual.TextStim(win=win, height=fixSize, units='deg')
face = visual.GratingStim(win=win, units='deg', size=faceSize, sf=1/faceSize, colorSpace='rgb')
blankImg = np.ones((330, 330)) * 101
flipTList, glitch=[],[]
# set up clock and keyboard
event.globalKeys.clear()
event.globalKeys.add(key='q', func=core.quit)  # global quit key
frameClock=clock.CountdownTimer()
globalClock = clock.Clock()
kb = keyboard.Keyboard(waitForStart=True, clock=globalClock) # create a keyboard object

# setup flip function
def firstflipfun(tk=None):
    kb.clock.reset()
    flipTList.append(globalClock.getTime()) # save flipTime
    if wantEyeTrack and tk is not None:
        tk.sendMessage('Exp starts')
        #tk.sendCommand('record_')

def flipfun(i, tk=None):
    flipTList.append(globalClock.getTime()) # save flipTime
    if wantEyeTrack and tk is not None:
        tk.sendMessage(f'Onset of frame {i}' )

def lastflipfun(tk=None):
    flipTList.append(globalClock.getTime()) # save flipTime
    if wantEyeTrack and tk is not None:
        tk.sendMessage(f'Exp end time' )

# ------------ now do it ----------------
print(f'Wait for trigger key {triggerKey}')
kb.start()
kb.waitKeys(keyList=[triggerKey])
print('Experiment starts: ....')
#for i in range(30): # loop frames    
for i in range(nMriFrame): # loop frames    
    # ----------- you really need to change this part -------
    # ----------- draw your all your stimulus ---------------
    # draw face
    img = images[:,:,imageId[i]] if imageId[i]!=-1 else blankImg
    #img = np.flipud(img)
    face.tex= img / 255 * 2 -1
    face.pos=allPosi[posiCond[i] if posiCond[i]!=-1 else 12] #以视角作为单位
    face.draw()
    
    # draw fixation
    fix.text=f'{digitId[i]}' # To do, 
    fix.color = (1,1,1) if i%2==0 else (-1,-1,-1) # alternate color 
    fix.draw()
    # -------------------------------------------------------


    # ------- deal with flip timing-------------
    if len(flipTList)==0: # 1st frame
        win.callOnFlip(firstflipfun, tk=tk)
        win.flip()
        expStartTime = flipTList[0]
        flipT = expStartTime
        whenDesired = expStartTime + mriFrameDur
        when = whenDesired
    else: # from 2nd frame         
        win.callOnFlip(flipfun, i=i, tk=tk)
        while 1:            
            if frameClock.getTime()<=0: # countdown time
                win.flip() # make the flip
                break
        
        flipT = flipTList[i]
        # deal with timing
        if (flipT-whenDesired) > refreshInterval * 0.5: # glitch
            glitch.append(1)
            whenDesired = whenDesired + mriFrameDur
        else: #no glitch
            glitch.append(0)
            whenDesired = flipT + mriFrameDur
        when = whenDesired-refreshInterval * timeFactor # note here we control the timing
    # update
    ttmp=globalClock.getTime()
    frameClock.reset()
    frameClock.add(when-ttmp)
# update the last frame and exp ends
win.callOnFlip(lastflipfun, tk=tk)
while 1:
    if frameClock.getTime()<=0: # countdown time
        win.flip() # make the flip
        break
expEndTime = flipTList[-1]
print(f'Experiment lasted {expEndTime-expStartTime} ')

# cleanup keyboard and eyetracker
if wantEyeTrack:
    closeupeyelinkmri(tk, outputfile=tmpEyeFile)
    rename(tmpEyeFile, fileName+'.edf')
kb.stop() # stop recording
keys=kb.getKeys() # collect all button press here
frameIntervals = win.frameIntervals
mri.update({'respKeys':keys, 'frameIntervals':frameIntervals, 'flipTList':flipTList, 'glitch':glitch, 'expStartTime':expStartTime, 'expEndTime':expEndTime})


# inspect timing
plt.plot(np.diff(flipTList))
plt.xlabel('Frame')
plt.ylabel('Duration')
plt.show()

# -------- save data ------------------
with open(f'{fileName}.pkl', 'wb') as f:
    pkl.dump(mri, f)
