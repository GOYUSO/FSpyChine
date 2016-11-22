try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    from tkinter import *

from FSM_class import *

from os.path import expanduser
home = expanduser("~")

def refresh(self,frame,inputs):

    # inputs = [
    #     ("Min number of bits", "vmin", Entry, 1),
    #     ("Max number of bits", "vmax", Entry, 3),
    #     ("Seed", "seed", Entry, "mySeed"),
    #     ("Number of states", "states", Entry, 5),
    #     ("Indeterminacy", "ind", Scale, 0.0),
    #     ("Loops", "loops", Scale, 0.0)
    # ]

    n = 2

    memo = []

    for text, value, f, default in inputs:
        label = Label(frame, text=text, bg=self.MAIN_COLOR)
        label.grid(row=n,column=3,sticky=E)
        memo.append(label)
        if f == Entry:
            if type(default) is int:
                self.results[value] = IntVar()
            else:
                self.results[value] = StringVar()
            t1 = f(frame, textvariable=self.results[value])
            t1.grid(row=n,column=4)
        if f == Scale:
            self.results[value] = IntVar()
            f(frame, orient=HORIZONTAL, sliderlength=20,variable=self.results[value], bg=self.MAIN_COLOR).grid(row=n,column=4)

        self.results[value].set(default)
        n += 1

    return memo


class App:

    def __init__(self,master):

        self.MAIN_COLOR = "#ffffff"
        self.SEC_COLOR = "#fff"

        self.frame = Frame(master, bg=self.MAIN_COLOR)
        self.frame.pack()

        try:
            self.input = self.input
        except AttributeError:
            self.input = [
                    ("Input (bits)", "vmin", Entry, 1),
                    ("Output (bits)", "vmax", Entry, 3),
                    ("Seed", "seed", Entry, "mySeed"),
                    ("Number of states", "states", Entry, 5),
                    ("Loops (%)", "loops", Scale, 0.0),
                    ("Jumps (%)", "jumps", Scale, 0.0)
                ]

        Label(
            self.frame, padx=10, pady=10 ,relief=RIDGE, text="FSpyChine",
            justify=CENTER, fg="#00aa00", background=self.SEC_COLOR).grid(row=0,columnspan=5)

        radios = [
            ("Random", 1),
            ("Sequential", 2),
            ("Patterns", 3)
        ]
        self.v = IntVar()
        self.v.set(1)
        n=2
        for text, value in radios:
            b = Radiobutton(self.frame, text=text, variable=self.v, value=value, command=self.radio_action, bg=self.MAIN_COLOR)
            b.grid(row=n, column=0, sticky=W)
            n += 1

        self.results = {}


        self.memo = refresh(self,self.frame,self.input)


        def exportKiss2():
            method_name = "fsm_" + str(self.v.get())
            method = getattr(self, method_name)
            return method()

        Label(self.frame, text="Path to export", bg=self.MAIN_COLOR).grid(row=6,column=0,sticky=E)
        self.results["path"] = StringVar()
        self.results["path"].set(home)

        t1 = Entry(self.frame, textvariable=self.results["path"])
        t1.grid(row=6,column=1)

        b1 = Button(master, text="Export kiss2", command=exportKiss2)
        # b1.pack()
        b1.pack()

        def image():
            method_name = "image_" + str(self.v.get())
            method = getattr(self, method_name)
            return method()

        b2 = Button(master, text="Export image", command=image)
        b2.pack()

        def getPatterns():
            method_name = "getPatterns"
            method = getattr(self, method_name)
            return method()

        b3 = Button(master, text="Get patterns", command=getPatterns)
        b3.pack()
        self.n = 0

    def getPatterns(self):
        if self.v.get() == 3:

            r = self.results
            x = FSM(
                seed = r["seed"].get(),
                input=r["vmin"].get(),
                output=r["vmax"].get(),
                states=r["states"].get(),
                loops=r["loops"].get())
            x.build(pattern)
            x.getPatterns()

        else:
            tkMessageBox.showinfo("This is not possible", "Sorry, but you must use this with a pattern FSM")

    def radio_action(self):
        # method_name = "fsm_" + str(self.v.get())
        # method = getattr(self, method_name)
        # return method()
        if self.v.get() == 3:
            self.memo[1].config(text='Number of patterns')
            self.memo[3].config(text='Max pattern length')
        else :
            self.memo[1].config(text='Output (bits)')
            self.memo[3].config(text='Number of states')


    def fsm_1(self):

        r = self.results
        x = FSM(
            seed=r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get())
        x.build(random)
        x.kiss2(r["path"].get())

    def fsm_2(self):
        r = self.results
        x = FSM(
            seed = r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            jumps=r["jumps"].get(),
            loops=r["loops"].get())
        x.build(sequential)
        x.kiss2(r["path"].get())

    def fsm_3(self):
        r = self.results
        x = FSM(
            seed = r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get())
        x.build(pattern)
        x.kiss2(r["path"].get())

    def image_1(self):
        r = self.results
        x = FSM(
            seed=r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get())
        x.build(random)
        x.image(r["path"].get())

    def image_2(self):
        r = self.results
        x = FSM(
            seed = r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            jumps=r["jumps"].get(),
            loops=r["loops"].get())
        x.build(sequential)
        x.image(r["path"].get())

    def image_3(self):
        r = self.results
        x = FSM(
            seed = r["seed"].get(),
            input=r["vmin"].get(),
            output=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get())
        x.build(pattern)
        x.image(r["path"].get())


root = Tk()
root.geometry("650x350")
root.title("FSpyChine -- Developed by Antonio Segura Cano")

app = App(root)

root.mainloop()