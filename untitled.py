from psychopy import core, monitors, clock, visual, event


mon= monitors.Monitor('ECNUmri')  #使用某种屏幕预设？
mon.setDistance(90)  # View distance cm
mon.setSizePix([1024, 768]) #
mon.setWidth(37)  # cm

win = visual.Window([1024, 768],units='deg', monitor=mon, checkTiming=True, colorSpace='rgb255',color=(101,101,101), allowGUI=False)

card_vert = [[0.5,0.5],[-0.5,0.5],[-0.5,-0.5],[0.5,-0.5]]
card=[];
for i in range(9):
    card.append(visual.ShapeStim(win, fillColor=(50,50,50),colorSpace='rgb255',vertices = card_vert))
    card[i].pos=((i-4)*1.5,0)

num= visual.TextStim(win,height =1,color = 'white',units='deg')

mymouse=event.Mouse(visible=True)
 
for i in range(9):
    card[i].draw()
    num.text=f'{i+1}'
    num.pos = ((i-4)*1.5,0)
    num.draw()


win.flip()
subres=0;
count=0;
while 1:
    for i in range(9):
        if mymouse.isPressedIn(card[i],buttons=[0]):
            subres=i+1;
            break
    if subres!=0:
        break
    

#core.wait(2)
win.close()

