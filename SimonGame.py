from tkinter import *
from Step import Step
from playsound import playsound
import threading
import random
from time import *
import pprint

class SimonGame(Step):
    def __init__(self, parent, data, stepname, blockCount):
        super().__init__(parent, data, stepname)
        self.blockCount = blockCount
        self.pp = pprint.PrettyPrinter(indent=4)

        self.cat = PhotoImage(file="img/cat.png")
        self.dog = PhotoImage(file="img/dog.png")
        self.bird = PhotoImage(file="img/bird.png")
        self.sheep = PhotoImage(file="img/sheep.png")

        self.description = Label(self, text="Status", font="Helvetica 16 bold italic")
        self.description.grid(sticky="W", row=0, column=1)

        self.catbutton = Button(self, command=lambda: self.catButtonPressedMouse(None))
        self.catbutton.config(image=self.cat)
        self.catbutton.image = self.cat
        self.catbutton.config(height=250, width=250)
        self.catbutton.grid(sticky="W", row=1, column=1)

        self.dogbutton = Button(self, command=lambda: self.dogButtonPressedMouse(None))
        self.dogbutton.config(image=self.dog)
        self.dogbutton.image = self.dog
        self.dogbutton.config(height=250, width=250)
        self.dogbutton.grid(sticky="W", row=2, column=0)

        self.birdbutton = Button(self, command=lambda: self.birdButtonPressedMouse(None))
        self.birdbutton.config(image=self.bird)
        self.birdbutton.image = self.bird
        self.birdbutton.config(height=250, width=250)
        self.birdbutton.grid(sticky="W", row=2, column=2)

        self.sheepbutton = Button(self, command=lambda: self.sheepButtonPressedMouse(None))
        self.sheepbutton.config(image=self.sheep)
        self.sheepbutton.image = self.sheep
        self.sheepbutton.config(height=250, width=250)
        self.sheepbutton.grid(sticky="W", row=3, column=1)

        self.catbutton.bind(self.catButtonPressedMouse)
        self.dogbutton.bind(self.dogButtonPressedMouse)
        self.birdbutton.bind(self.birdButtonPressedMouse)
        self.sheepbutton.bind(self.sheepButtonPressedMouse)

        self.btnstrlst = ['cat', 'dog', 'bird', 'sheep']
        self.target_mem_seq = []
        self.curr_target_index = -1
        self.trialCount = 0
        self.blockList = []
        self.currentIndex = 0
        self.schedule = [(2000, lambda: self.labelnexttrial()),
                         (2000, lambda: self.labelbeginAnimation())]
        self.completed = False
        self.animDone = False

    def runBlock(self):
        print('Blockcount: ', self.blockCount)
        if self.blockCount <= 3:
            # self.blockCount += 1
            self.blockList.clear()
            self.generateBlockSeq()
            self.nextTrial()
        else:
            self.schedule.clear()
            self.schedule = [(200, lambda: self.gameOver())]
            self.doanim()
            self._step_completed()
        # TODO: disable button while animation playing and enable button when animation ends

    def nextTrial(self):
        self.schedule.clear()
        self.curr_target_index = 0
        print('Trial: '+ str(self.trialCount))
        print('Data Dict: ')
        self.pp.pprint(self.data)
        if self.trialCount <= 2:
            self.trialCount += 1
            self.data[self.stepname]['Trial' + str(self.trialCount)] = {}
            self.target_mem_seq = self.blockList[self.trialCount - 1]
            self.data[self.stepname]['Trial' + str(self.trialCount)]['Target'] = self.target_mem_seq
            self.data[self.stepname]['Trial' + str(self.trialCount)]['UserInput'] = []
            self.schedule = [(2000, lambda: self.labelnexttrial()),
                             (2000, lambda: self.labelbeginAnimation())]
            self.generateTrialSche()
            self.doanim()
        else:
            print('--------------------------TODO: CALL WORKLOAD ASSESS-----------------------')
            self._step_completed()
            self.schedule.clear()
            self.schedule = [(2000, lambda: self.label_game_over())]
            self.doanim()

    def generateBlockSeq(self):
        for i in range(0, 5):
            trialEle = []
            for x in range(0, self.blockCount * 3):
                trialEle.append(random.choice(self.btnstrlst))
            self.blockList.append(trialEle)
        print('Generated block list:', self.blockList)
        print('In generate - Block count: ', self.blockCount)

    def generateTrialSche(self):
        for str in self.target_mem_seq:
            print('anim str:', str)
            if str == 'cat':
                self.schedule.append((700, lambda: self.btnPressed(None, self.catbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.catbutton)))
            if str == 'dog':
                self.schedule.append((700, lambda: self.btnPressed(None, self.dogbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.dogbutton)))
            if str == 'sheep':
                self.schedule.append((700, lambda: self.btnPressed(None, self.sheepbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.sheepbutton)))
            if str == 'bird':
                self.schedule.append((700, lambda: self.btnPressed(None, self.birdbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.birdbutton)))
        self.schedule.append((500, lambda: self.labelstartGame()))

    def doanim(self):
        if len(self.schedule) <= 0:
            return
        self.sched_item = 0
        s = self.schedule[self.sched_item]
        # run the function stored in the schedule
        self.after(s[0], self.doanim_helper)
        # self.after(2000, self.enable_button())
        print('between: ', self.animDone)
        self.animDone = True
        print('between2: ', self.animDone)

    def doanim_helper(self):
        s = self.schedule[self.sched_item]
        # run the function stored in the schedule
        s[1]()
        self.sched_item += 1
        if self.sched_item < len(self.schedule):
            s = self.schedule[self.sched_item]
            self.after(s[0], self.doanim_helper)

    def btn_action(self, btn_name):
        print('----------------------in btn_action------------------------')
        print('trial count: ', self.trialCount)
        print('user picked: ', btn_name)
        print('target_mem_seq: ', self.target_mem_seq)
        print('target btn: ', self.target_mem_seq[self.curr_target_index])
        print('curr_target_index: ', self.curr_target_index)
        if btn_name != self.target_mem_seq[self.curr_target_index]:
            print("Failure!!!")
            self.description.config(text='Wrong answer!', fg='red')
            self.data[self.stepname]['Trial' + str(self.trialCount)]['TrialResult'] = 'Failure'
            self.nextTrial()
        elif self.curr_target_index >= len(self.target_mem_seq) - 1:
            print("Success!!")
            self.description.config(text='Success!', fg='green')
            self.data[self.stepname]['Trial' + str(self.trialCount)]['TrialResult'] = 'Success'
            self.nextTrial()
        else:
            print("Good so far...")
            self.description.config(text='Good so far...', fg='yellow')
            self.curr_target_index += 1

    def disable_button(self):
        self.catbutton.config(state=DISABLED)
        self.birdbutton.config(state=DISABLED)
        self.dogbutton.config(state=DISABLED)
        self.sheepbutton.config(state=DISABLED)

    def enable_button(self):
        self.catbutton.config(state='normal')
        self.birdbutton.config(state='normal')
        self.dogbutton.config(state='normal')
        self.sheepbutton.config(state='normal')

    def catButtonPressedMouse(self, event):
        self.btnPressed(None, self.catbutton)
        self.after(1000, self.catButtonReleasedMouse)
        self.data[self.stepname]['Trial' + str(self.trialCount)]['UserInput'].append('Cat: ' + strftime("%Y-%m-%d %H:%M:%S",
                                                                                                gmtime()))
        self.btn_action('cat')

    def catButtonReleasedMouse(self):
        self.btnReleased(None, self.catbutton)

    def dogButtonPressedMouse(self, event):
        self.btnPressed(None, self.dogbutton)
        self.after(800, self.dogButtonReleasedMouse)
        self.data[self.stepname]['Trial' + str(self.trialCount)]['UserInput'].append('Dog: ' + strftime("%Y-%m-%d %H:%M:%S",
                                                                                                gmtime()))
        self.btn_action('dog')

    def dogButtonReleasedMouse(self):
        self.btnReleased(None, self.dogbutton)

    def birdButtonPressedMouse(self, event):
        self.btnPressed(None, self.birdbutton)
        self.after(1000, self.birdButtonReleasedMouse)
        self.data[self.stepname]['Trial' + str(self.trialCount)]['UserInput'].append('Bird: ' + strftime("%Y-%m-%d %H:%M:%S",
                                                                                                gmtime()))
        self.btn_action('bird')

    def birdButtonReleasedMouse(self):
        self.btnReleased(None, self.birdbutton)

    def sheepButtonPressedMouse(self, event):
        self.btnPressed(None, self.sheepbutton)
        self.after(1000, self.sheepButtonReleasedMouse)
        self.data[self.stepname]['Trial' + str(self.trialCount)]['UserInput'].append('Sheep: ' + strftime("%Y-%m-%d %H:%M:%S",
                                                                                                gmtime()))
        self.btn_action('sheep')

    def sheepButtonReleasedMouse(self):
        self.btnReleased(None, self.sheepbutton)

    def onscreen_enter(self):
        super().onscreen_enter()
        self.runBlock()

    def labelbeginAnimation(self):
        self.description.config(text="Animation is playing...", fg='blue')

    def labelstartGame(self):
        self.description.config(text="Now it's your turn. Go!", fg='blue')

    def labelnexttrial(self):
        self.description.config(text='Waiting to start next trial...', fg='black')

    def label_success(self):
        self.description.config(text="Success!", fg='green')

    def label_fail(self):
        self.description.config(text="You failed this trial", fg='red')

    def label_game_over(self):
        self.description.config(text="Trial finished! (Press next to continue)", fg='red')

    def btnPressed(self, event, btn):
        if btn == self.catbutton:
            self.catbutton.config(highlightbackground='red')
            t1 = threading.Thread(target=playsound, args=['audio/cat.wav'])
            t1.start()
        if btn == self.dogbutton:
            self.dogbutton.config(highlightbackground='blue')
            t1 = threading.Thread(target=playsound, args=['audio/dog.wav'])
            t1.start()
        if btn == self.sheepbutton:
            self.sheepbutton.config(highlightbackground='black')
            t1 = threading.Thread(target=playsound, args=['audio/sheep.wav'])
            t1.start()
        if btn == self.birdbutton:
            self.birdbutton.config(highlightbackground='yellow')
            t1 = threading.Thread(target=playsound, args=['audio/bird.wav'])
            t1.start()

    def btnReleased(self, event, btn):
        if btn == self.catbutton:
            self.catbutton.config(highlightbackground='#FFFFFF')
        if btn == self.dogbutton:
            self.dogbutton.config(highlightbackground='#FFFFFF')
        if btn == self.birdbutton:
            self.birdbutton.config(highlightbackground='#FFFFFF')
        if btn == self.sheepbutton:
            self.sheepbutton.config(highlightbackground='#FFFFFF')