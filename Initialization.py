from tkinter import *
from Step import Step
import datetime

class Init(Step):
    def __init__(self, parent, data, stepname):
        super().__init__(parent, data, stepname)

        now = datetime.datetime.now()
        self.curTime = Label(self, text=now.strftime("%Y-%m-%d %H:%M"))
        self.curTime.pack()

        Label(self, text="Participant ID").pack()
        self.pIDtext = StringVar()
        vcmd1 = (self.register(self.updatePID), '%P')
        self.pID = Entry(self, textvariable=self.pIDtext, validate="key", validatecommand=vcmd1)
        self.pID.pack()

        Label(self, text="Session ID").pack()
        self.sessionIDtext = StringVar()
        vcmd2 = (self.register(self.updateSessionID), '%P')
        self.sessionID = Entry(self, textvariable=self.sessionIDtext, validate="key", validatecommand=vcmd2)
        self.sessionID.pack()

        self.data[self.stepname]["pID"] = self.pID.get()
        self.data[self.stepname]["session ID"] = self.sessionID.get()
        self.data[self.stepname]["current time"] = now.strftime("%Y-%m-%d %H:%M")

    def updatePID(self, new_text):
        self.data[self.stepname]["pID"] = new_text
        return True

    def updateSessionID(self, new_text):
        self.data[self.stepname]["session ID"] = new_text
        return True

