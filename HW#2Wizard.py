from tkinter import *

from Wizard import Wizard

from WorkloadAssess import Weighting
from WorkloadAssess import Ranking
from Initialization import Init
from SimonGame import SimonGame


class hw2Wizard(Wizard):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        steps = [Init(self, self.data, "Initialization Data"),
                 SimonGame(self, self.data, 'Block1', 1),
                 Weighting(self, self.data, 'TLX Score', 1),
                 Ranking(self, self.data, 'Ranking Comparison', 1),

                 SimonGame(self, self.data, 'Block2', 2),
                 Weighting(self, self.data, 'TLX Score', 2),
                 Ranking(self, self.data, 'Ranking Comparison', 2),

                 SimonGame(self, self.data, 'Block3', 3),
                 Weighting(self, self.data, 'TLX Score', 3),
                 Ranking(self, self.data, 'Ranking Comparison', 3)]

        self.set_steps(steps)
        self.start()

if __name__ == "__main__":
    root = Tk()

    data = {}
    hw2_gui = hw2Wizard(root, data)
    hw2_gui.pack()

    root.mainloop()
