from Tkinter import *
from FSM_class import *
class App:

    def __init__(self,master):

        self.MAIN_COLOR = "#ffffff"
        self.SEC_COLOR = "#fff"

        frame = Frame(master, bg=self.MAIN_COLOR)
        frame.pack()

        Label(
            frame, padx=10, pady=10 ,relief=RIDGE, text="Please, select a FSM",
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
            b = Radiobutton(frame, text=text, variable=self.v, value=value, command=self.radio_action, bg=self.MAIN_COLOR)
            b.grid(row=n, column=0, sticky=W)
            n += 1

        self.results = {}

        inputs = [
            ("Min number of bits", "vmin", Entry, 1),
            ("Max number of bits", "vmax", Entry, 3),
            ("Seed", "seed", Entry, "mySeed"),
            ("Number of states", "states", Entry, 5),
            ("Indeterminacy", "ind", Scale, 0.0),
            ("Loops", "loops", Scale, 0.0)
        ]

        n = 2

        for text, value, f, default in inputs:
            Label(frame, text=text, bg=self.MAIN_COLOR).grid(row=n,column=3,sticky=E)
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

        # CANVAS

        # self.canvas = {"width":150,"height":100,"rects":10, "rectangles":[]}
        # w = Canvas(frame, bd=1, relief=GROOVE, width=self.canvas["width"], height=self.canvas["height"])
        # # w.grid(column=0,rowspan=1)
        #
        # n = self.canvas["rects"]
        # nw = self.canvas["width"] / n
        # w.create_line(0, 100, 200, 100)
        #
        # values = [0,0.1,0.1,0.2,0.2,0.1,0,0.1,0.1,0.1]
        # hvalue = self.canvas["height"]/100
        #
        # def callback(event):
        #     canvas = event.widget
        #
        #     x = canvas.canvasx(event.x)
        #     y = canvas.canvasy(event.y)
        #     print x
        #     print canvas.find_closest(x, y)
        #
        # for rect in range(n):
        #     mheight = values[rect]*hvalue*self.canvas["height"]
        #     rect = w.create_rectangle(rect*nw+nw/2,self.canvas["height"]-mheight-1,rect*nw+nw,self.canvas["height"],fill="blue", tags=str(rect))
        #     w.tag_bind(str(rect),None,callback)
        #     print rect
        #
        # w.grid(column=0,rowspan=1)


        # w.create_rectangle(0,0,50,100,fill="red")

        # ENDCANVAS




    def radio_action(self):
        method_name = "fsm_" + str(self.v.get())
        method = getattr(self, method_name)
        return method()

    def fsm_1(self):
        r = self.results
        FSM(
            seed=r["seed"].get(),
            min=r["vmin"].get(),
            max=r["vmax"].get(),
            states=r["states"].get(),
            indeterminacy=r["ind"].get(),
            loops=r["loops"].get()).build(random)
        print "random"

    def fsm_2(self):
        r = self.results
        FSM(
            seed = r["seed"].get(),
            min=r["vmin"].get(),
            max=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get()).build(sequential)

        print "sequential"

    def fsm_3(self):
        r = self.results
        FSM(
            seed = r["seed"].get(),
            min=r["vmin"].get(),
            max=r["vmax"].get(),
            states=r["states"].get(),
            loops=r["loops"].get()).build(pattern)
        print "patterns"


root = Tk()
root.geometry("500x500")
root.title("FSpyChine -- Developed by Antonio Segura Cano")

app = App(root)

root.mainloop()