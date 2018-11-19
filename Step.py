from tkinter import Tk, Label, Radiobutton, Button, StringVar, Entry, Scale, IntVar, END, W, E, HORIZONTAL, LEFT, Frame, SUNKEN


class Step(Frame):
    def __init__(self, parent, data, stepname):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        self.stepname = stepname

        if not stepname in self.data:
            self.data[stepname] = {}

        self.completed = True
        self.previous_enabled = True

    # Wizard Steps should call this once it is ok to advance to the next step
    # Will result in the "Next" or "Finish" buttons becoming enabled/interactive/not grayed out
    def _step_completed(self):
        self.completed = True
        self.parent.event_generate("<<step_complete>>", when="tail")

    # The Wizard calls this for the Step when it comes into view
    def onscreen_enter(self):
        pass

    # The Wizard calls this for the Step when it is removed from view
    def onscreen_exit(self):
        pass

    def allow_previous(self):
        return self.previous_enabled

    def allow_next(self):
        return self.completed
