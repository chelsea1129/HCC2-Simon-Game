from tkinter import *
from Step import Step
from playsound import playsound
from WorkloadAssess import Weighting
from WorkloadAssess import Ranking
import threading
import random
import pprint

class Game(Step):
    def __init__(self, parent, data, stepname):
        super().__init__(parent, data, stepname)

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
        self.blockCount = 0
        self.trialCount = 0
        self.blockList = []
        self.currentIndex = 0
        self.schedule = [(2000, lambda: self.labelnexttrial()),
                         (2000, lambda: self.labelbeginAnimation())]

        self.completed = False

    def runWorkloadAssess(self):
        Weighting(self, self.data, "TLX Score")
        Ranking(self, self.data, "Ranking")

    def runBlock(self):
        print('-----------------in runBlock----------------')
        print('block count: ', self.blockCount)
        print('trial count: ', self.trialCount)
        # self.disable_button()
        self.blockCount += 1
        if self.blockCount <= 3:
            self.runWorkloadAssess()
            self.blockList.clear()
            self.addingToList(self.blockCount * 3)
            print('new block list: ', self.blockList)
            self.nextTrial()
        else:
            self.schedule.clear()
            self.schedule = [(200, lambda: self.gameOver())]
            self.doanim()
            self._step_completed()

    def generateSchedule(self):
        self.generateAndPlayAnim()
        self.schedule.append((200, lambda: self.labelstartGame()))
        # self.enable_button()

    def nextTrial(self):
        print('---------------next trial------------------')
        print('block count: ', self.blockCount)
        print('trial count: ', self.trialCount)
        self.curr_target_index = 0
        if self.trialCount >= 5:
            print('run a new block')
            self.trialCount = 0
            self.runBlock()
        else:
            print('continue new trial')
            self.trialCount += 1
            self.target_mem_seq = self.blockList[self.trialCount - 1]
            self.schedule.clear()
            self.schedule = [(2000, lambda: self.labelnexttrial()),
                             (2000, lambda: self.labelbeginAnimation())]
            self.generateSchedule()
            self.doanim()

    def addingToList(self, count):
        print('--------------------in addingToList---------------')
        for i in range(0, 5):
            trialEle = []
            for x in range(0, count):
                trialEle.append(random.choice(self.btnstrlst))
            self.blockList.append(trialEle)
            print('block list: ', self.blockList)
        print('--------------------------------------------------')

    def generateAndPlayAnim(self):
        for str in self.target_mem_seq:
            print('anim str:', str)
            if str == 'cat':
                self.schedule.append((1000, lambda: self.btnPressed(None, self.catbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.catbutton)))
            if str == 'dog':
                self.schedule.append((1000, lambda: self.btnPressed(None, self.dogbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.dogbutton)))
            if str == 'sheep':
                self.schedule.append((1000, lambda: self.btnPressed(None, self.sheepbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.sheepbutton)))
            if str == 'bird':
                self.schedule.append((1000, lambda: self.btnPressed(None, self.birdbutton)))
                self.schedule.append((500, lambda: self.btnReleased(None, self.birdbutton)))
        self.schedule.append((500, lambda: self.labelstartGame()))

    def btn_action(self, btn_name):
        print('----------------------in btn_action------------------------')
        print('block count: ', self.blockCount)
        print('trial count: ', self.trialCount)
        print('user picked: ', btn_name)
        print('target_mem_seq: ', self.target_mem_seq)
        print('target btn: ', self.target_mem_seq[self.curr_target_index])
        print('curr_target_index: ', self.curr_target_index)
        if btn_name != self.target_mem_seq[self.curr_target_index]:
            print("Failure!!!")
            self.data[self.stepname]['Block ', self.blockCount, ', Trial ', self.trialCount] = 'Failure'
            self.description.config(text='Wrong answer!', fg='red')
            # self.description.config(text='Trial complete!', fg='blue')
            self.nextTrial()
        elif self.curr_target_index >= len(self.target_mem_seq) - 1:
            print("Success!!")
            self.data[self.stepname]['Block ', self.blockCount, ', Trial ', self.trialCount] = 'Success'
            self.description.config(text='Success!', fg='green')
            # self.description.config(text='Trial complete!', fg='blue')
            self.nextTrial()
        else:
            print("Good so far...")
            self.description.config(text='Good so far...', fg='yellow')
            self.curr_target_index += 1
        print('------------------------btn_action ends------------------')

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

    def catButtonPressedMouse(self, event):
        self.btnPressed(None, self.catbutton)
        self.after(1000, self.catButtonReleasedMouse)
        self.btn_action('cat')

    def catButtonReleasedMouse(self):
        self.btnReleased(None, self.catbutton)

    def dogButtonPressedMouse(self, event):
        self.btnPressed(None, self.dogbutton)
        self.after(800, self.dogButtonReleasedMouse)
        self.btn_action('dog')

    def dogButtonReleasedMouse(self):
        self.btnReleased(None, self.dogbutton)

    def birdButtonPressedMouse(self, event):
        self.btnPressed(None, self.birdbutton)
        self.after(1000, self.birdButtonReleasedMouse)
        self.btn_action('bird')

    def birdButtonReleasedMouse(self):
        self.btnReleased(None, self.birdbutton)

    def sheepButtonPressedMouse(self, event):
        self.btnPressed(None, self.sheepbutton)
        self.after(1000, self.sheepButtonReleasedMouse)
        self.btn_action('sheep')

    def sheepButtonReleasedMouse(self):
        self.btnReleased(None, self.sheepbutton)

    def onscreen_enter(self):
        super().onscreen_enter()
        self.runBlock()


    def doanim(self):
        print('start animation')
        print(self.schedule)
        if len(self.schedule) <= 0:
            return

        self.sched_item = 0

        s = self.schedule[self.sched_item]
        #run the function stored in the schedule
        self.after(s[0], self.doanim_helper)
        # self.after(2000, self.enable_button())

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


    def doanim_helper(self):
        s = self.schedule[self.sched_item]
        # run the function stored in the schedule
        s[1]()

        self.sched_item += 1

        if self.sched_item < len(self.schedule):
            # self.after(1000, self.start_game)
        # else:
            s = self.schedule[self.sched_item]
            self.after(s[0], self.doanim_helper)


    def labelbeginAnimation(self):
        self.description.config(text="Animation is playing...", fg='blue')

    def labelstartGame(self):
        self.description.config(text="Now it's your turn. Go!", fg='blue')

    def labelnexttrial(self):
        self.description.config(text='Waiting to start next trial...', fg='yellow')

    def label_success(self):
        self.description.config(text="Success!", fg='green')

    def label_fail(self):
        self.description.config(text="You failed this trial", fg='red')

    def gameOver(self):
        self.description.config(text="Game over", fg='red')
