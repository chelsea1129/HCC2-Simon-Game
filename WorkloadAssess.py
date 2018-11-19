from tkinter import *
from Step import Step
import random

class Weighting(Step):
    def __init__(self, parent, data, stepname, blockCount):
        super().__init__(parent, data, stepname)
        self.blockCount = blockCount
        self.data['Block' + str(self.blockCount)][self.stepname] = {}
        self.completed = False
        # self.Q1 = False
        # self.Q2 = False
        # self.Q3 = False
        # self.Q4 = False
        # self.Q5 = False
        # self.Q6 = False
        # self.completed = self.Q1 and self.Q2 and self.Q3 and self.Q4 and self.Q5 and self.Q6

        lbl1 = Label(self, text="1. How much mental and perceptual activity was required (e.g. thinking, deciding, calculating, remembering, looking, searching, etc)?", anchor='w')
        lbl1.pack(side="top", fill="both")
        lbl2 = Label(self, text="    Was the task easy or demanding, simple or complex, exacting or forgiving?", anchor='w')
        lbl2.pack(fill="both")
        lbl3 = Label(self, text="Mental Demand (1 as low, 20 as high)")
        lbl3.pack()
        mentScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL, command=self.updateMentVal)
        mentScore.set(3)
        mentScore.pack()
        print(self.data)
        self.data['Block' + str(self.blockCount)][self.stepname]["mental demand"] = mentScore.get()

        Label(self,
              text="2. How much physical activity was required (e.g. pushing, pulling, turning, controlling, activating, etc)? ",
              anchor='w').pack(fill='both')
        Label(self, text="    Was the task easy or demanding, slow or brisk, slack or strenuous, restful or laborious?",
              anchor='w').pack(fill='both')
        Label(self, text="Physical Demand (1 as low, 20 as high)").pack()
        phyScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL, command=self.updatePhyVal)
        phyScore.set(3)
        phyScore.pack()
        self.data['Block' + str(self.blockCount)][self.stepname]["physical demand"] = phyScore.get()

        Label(self,
              text="3. How much time pressure did you feel due to the rate of pace at which the tasks or task elements occurred?",
              anchor='w').pack(fill='both')
        Label(self, text="    Was the pace slow and leisurely or rapid and frantic?", anchor='w').pack(fill='both')
        Label(self, text="Temporal Demand (1 as low, 20 as high)").pack()
        tempScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL, command=self.updateTempVal)
        tempScore.set(3)
        tempScore.pack()
        self.data['Block' + str(self.blockCount)][self.stepname]["temporal demand"] = tempScore.get()

        Label(self,
              text="4. How successful do you think you were in accomplishing the goals of the task set by the experimenter (or yourself)?",
              anchor='w').pack(fill='both')
        Label(self, text="    How satisfied were you with your performance in accomplishing these goals?", anchor='w').pack(fill='both')
        Label(self, text="Performance(1 as low, 20 as high)").pack()
        performScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL,
                            command=self.updatePerformVal)
        performScore.set(3)
        performScore.pack()
        self.data['Block' + str(self.blockCount)][self.stepname]["performance"] = performScore.get()

        Label(self,
              text="5. How hard did you have to work (mentally and physically) to accomplish your level of performance?",
              anchor='w').pack(fill='both')
        Label(self, text="Effort(1 as low, 20 as high)").pack()
        effortScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL,
                            command=self.updateEffVal)
        effortScore.set(3)
        effortScore.pack()
        self.data['Block' + str(self.blockCount)][self.stepname]["effort"] = effortScore.get()

        Label(self,
              text="6. How insecure, discouraged, irritated, stressed and annoyed versus secure, gratified, content, relaxed and complacent did you feel during the task?",
              anchor='w').pack(fill='both')
        Label(self, text="Frustration(1 as low, 20 as high)").pack()
        frustScore = Scale(self, from_=1, to=20, length=600, tickinterval=1, orient=HORIZONTAL,
                            command=self.updateFrustVal)
        frustScore.set(3)
        frustScore.pack()
        self.data['Block' + str(self.blockCount)][self.stepname]["frustration score"] = frustScore.get()

    def updateMentVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["mental demand"] = event

    def updatePhyVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["physical demand"] = event

    def updateTempVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["temporal demand"] = event

    def updatePerformVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["performance score"] = event

    def updateEffVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["effort score"] = event

    def updateFrustVal(self, event):
        self.data['Block' + str(self.blockCount)][self.stepname]["frustration score"] = event
        self._step_completed()

    def onscreen_enter(self):
        super().onscreen_enter()
        # if self.completed:
        #     self._step_completed()


class Ranking(Step):
    def __init__(self, parent, data, stepname, blockCount):
        super().__init__(parent, data, stepname)
        self.blockCount = blockCount
        self.data['Block' + str(self.blockCount)][self.stepname] = {}

        self.compareStrLst = []
        self.updateFactorsFunc = []
        for i in range(0, 15):
            tempStr = StringVar()
            self.compareStrLst.append(tempStr)
            i = i + 1

        self.factorList = ["Frustration", "Physical Demand", "Mental Demand", "Temporal Demand", "Performance", "Effort"]
        factor_pairs = self.choosetwo(self.factorList)
        shuffled_pairs = self.shuffle(factor_pairs)

        self.intro=Label(self, text='Click on the factor that represents the more important contributor to workload for the task.')
        self.intro.grid(sticky='W', row=0, column=0, columnspan=3)
        print(shuffled_pairs)
        self.compareFactors(shuffled_pairs)

    def choosetwo(self, lst):
        res = []
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                tup = (lst[i], lst[j])
                res.append(tup)
        return res

    def shuffle(self, lst):
        l = lst
        res = []
        while len(l) > 0:
            index = random.randint(0, len(l) - 1)
            res.append(l[index])
            del l[index]
        return res

    def updateFactors(self, i):
        self.data['Block' + str(self.blockCount)][self.stepname]['Comparison'+str(i)] = self.compareStrLst[i-1].get()


    def compareFactors(self, lst):
        qnum = 1
        for pair in lst:
            print('qnum: ', qnum)
            print('current pair: ', pair)
            qnumLbl = Label(self, text=str(qnum) + '.')
            qnumLbl.grid(sticky='W', row=qnum, column=0)

            compareFct = self.compareStrLst[qnum - 1]
            print(compareFct)
            factor1 = Radiobutton(self, text=pair[0], variable=compareFct, value=pair[0],
                                  command=lambda i=qnum: self.updateFactors(i))
            factor1.grid(sticky='W', row=qnum, column=1)
            factor2 = Radiobutton(self, text=pair[1], variable=compareFct, value=pair[1],
                                  command=lambda i=qnum: self.updateFactors(i))
            factor2.grid(sticky='W', row=qnum, column=2)

            self.data['Block' + str(self.blockCount)][self.stepname]['Comparison' + str(qnum)] = compareFct.get()
            qnum = qnum + 1
