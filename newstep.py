from tkinter import *

from Step import Step

# A partial example of how to use the new Wizard+Step

class newstep(Step):
    def __init__(self, parent, data, stepname):
        super().__init__(parent, data, stepname)

        # tell the wizard that this step will NOT allow the "Next/Finish" button
        # to be pressed until _step_completed() is called at some later time
        self.completed = False


    # The Wizard calls this for the Step when it comes into view
    # A good time to start animations!
    def onscreen_enter(self):
        super().onscreen_enter()

        # Example: self.doanim()

        self._step_completed()



