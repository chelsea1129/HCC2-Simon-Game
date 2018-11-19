from tkinter import Tk, Button, Frame

class Wizard(Frame):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.parent = parent

        self.current_step = None
        self.current_step_index = 0

        self.steps = []
        self.data = data

        self.button_frame = Frame(self, bd=1, relief="raised")
        self.content_frame = Frame(self)

        self.back_button = Button(self.button_frame, text="<< Back", command=self.back)
        self.next_button = Button(self.button_frame, text="Next >>", command=self.next)
        self.finish_button = Button(self.button_frame, text="Finish", command=self.finish)

        #self.content_frame.pack_propagate(0)  # Don't allow the widgets inside to determine the frame's width / height
        self.content_frame.pack(side="top", fill="both", expand=True)

        #self.button_frame.pack_propagate(0)
        self.button_frame.pack(side="bottom", fill="x")

        print("wizard bound to step_complete event")
        self.bind("<<step_complete>>", self.step_complete)

        # Example custom event call for above bind()
        # self.event_generate("<<step_complete>>", when="tail")


    def step_complete(self, event):
        #print("Wizard:step_complete()")
        self.next_button.config(state="normal")
        self.finish_button.config(state="normal")



    def set_steps(self, steps):
        self.steps = steps

    def start(self):
        self.show_step(self.current_step_index)

    def back(self):
        self.current_step_index -= 1
        self.show_step(self.current_step_index)

    def next(self):
        self.current_step_index += 1
        self.show_step(self.current_step_index)

    def finish(self):
        self.current_step_index = 0

        print("data is: ")
        print(self.data)

        self.parent.quit()

    def show_step(self, step):

        if step < len(self.steps):
            if self.current_step is not None:
                # remove current step
                self.current_step.onscreen_exit()
                self.current_step.pack_forget()

            self.current_step = self.steps[step]
            self.current_step.pack(fill="both", expand=True)
            self.current_step.onscreen_enter()


        if len(self.steps) != 0:
            if len(self.steps) == 1:
                self.back_button.pack_forget()
                self.next_button.pack_forget()
                self.finish_button.pack(side="right")
            elif step == 0:
                # first step
                self.back_button.pack_forget()
                self.next_button.pack(side="right")
                self.finish_button.pack_forget()

            elif step == len(self.steps)-1:
                # last step
                self.back_button.pack(side="left")
                self.next_button.pack_forget()
                self.finish_button.pack(side="right")

            else:
                # all other steps
                self.back_button.pack(side="left")
                self.next_button.pack(side="right")
                self.finish_button.pack_forget()
        else:
            self.back_button.pack_forget()
            self.next_button.pack_forget()
            self.finish_button.pack(side="right")

        if self.current_step is not None:
            if self.current_step.allow_next():
                self.next_button.config(state="normal")
                self.finish_button.config(state="normal")
            else:
                self.next_button.config(state="disabled")
                self.finish_button.config(state="disabled")

            if not self.current_step.allow_previous():
                self.back_button.pack_forget()

if __name__ == "__main__":
    from DemoStep import DemoStep

    root = Tk()

    data = {}
    my_gui = Wizard(root, data)
    steps = [DemoStep(my_gui, data, "one"), DemoStep(my_gui, data, "two"), DemoStep(my_gui, data, "three")]
    #steps = [DemoStep(my_gui, data, "one")]
    #steps = []
    my_gui.set_steps(steps)
    my_gui.pack()
    my_gui.start()

    root.mainloop()
