__author__ = 'Antonio Segura Cano'

import numpy as np
import time

from graphviz import Digraph

import tkMessageBox

from wildcards import wildcard

from FSM_utils import *

# We'll create a FSMachine class
# FSMachine class will generate all methods about the program
# A random FSMachine: FSMachine.random

#     KISS2 headers include the following information:
#
#     .i    # number of inputs
#     .o    # number of outputs
#     .p    # number of products
#     .s    # number of states used
#     .r    # RESET state [optional]


class FSM:
    def __init__(self, **kwargs):

        self.meta = kwargs
        self.statesdict = {}

    def build(self, f):
        self.statesdict = f(self.meta)

    def kiss2(self, *args):
        filename = time.strftime("FSM_%m%d%H%M%S.kiss2")
        if args:
            path = args[0]
        stated = self.statesdict
        if not stated:
            stated = self.meta["statesdict"]
        # name = time.strftime("FSM_%m%d%H%M%S.kiss2")
        if stated.__len__() != 0:
            p = 0
            i = False
            o = False
            outfile = open(path + "/" + filename, 'a')
            blob = ""
            for statenode in stated:
                if not i or not o or not r:
                    i = stated[statenode][0][1].__len__()
                    o = stated[statenode][0][2].__len__()
                    r = statenode
                for transition in stated[statenode]:
                    t2 = transition[2]
                    if self.meta["type"] == "pattern":
                        t2 = int(transition[2])
                        t2 = "{0:b}".format(t2)
                        while t2.__len__() < math.log(self.meta["output"]-1) + 1:
                            t2 = "0"+t2
                    blob += transition[1] + " " + statenode + " " + transition[0] + " " + t2 + "\n"
                    p += 1
            iopsr = [i,o,p,stated.__len__(),r]
            header = "iopsr"
            cont = 0
            for l in header:
                outfile.write("." + l + " " + str(iopsr[cont]) + "\n")
                cont += 1
            outfile.write("\n"+blob)
        else:
            print "Sorry, but you must create a FSM with 'built' method first"

    def image(self, *args):
        filename = time.strftime("FSM_%m%d%H%M%S")

        if args:
            path = args[0]

        infile = self.statesdict
        if not infile:
            infile = self.meta["statesdict"]

        dot = Digraph(directory=path)
        # dot.directory = path
        dot.filename = filename
        dot.format = 'png'


        for state in infile:
            dot.node(state, state)

        for state in self.statesdict:
            dot.edge("",state)
            break

        for state in infile:
            for edge in infile[state]:
                dot.edge(state,edge[0],edge[1] + ' / ' + edge[2])

        dot.view()
        try:
            dot.render(filename, view=True)
        except IOError:
            pass

    def getPatterns(self, *args):
        filename = time.strftime("Patterns_FSM_%m%d%H%M%S.txt")
        if args:
            path = args[0]

        outfile = open(path + "/" + filename, 'a')

        msg = self.meta["patternlist"]
        message = ""
        cont = 1
        for i in msg:
            message += str(cont) + " -> " + i + "\n"
            cont += 1

        outfile.write(message)

        tkMessageBox.showinfo("The patterns are the following: ", message)

    def __makeindeterminacy(cls, *args):
        if args:
            ind = args[0]*100
            npri = np.random.random_integers

            for state in cls.statesdict:
                res = []
                for edge in cls.statesdict[state]:
                    if not hasindeterminacy(edge):
                        count = 0
                        ledge = list(edge[1])
                        for bit in ledge:
                            percent = npri(0,100) # 0 and 100 are both included
                            if percent <= ind:
                                ledge[count] = '-'
                            count += 1
                        lst = list (edge)
                        lst[1] = "".join(ledge)
                        edge = tuple (lst)
                        res.append(edge)
                cls.statesdict[state] = res
                actualstatelist = list(cls.statesdict[state])
                count = 0
                for s0 in actualstatelist:
                    anotherstates = list(actualstatelist)
                    del anotherstates[count]
                    count += 1
                    c = 0
                    for s1 in anotherstates:
                        if matchindeterminacy(s0[1],s1[1]):
                            del anotherstates[c]
                        c += 1
                        # MAKE INDETERMINACY
            for state in cls.statesdict:
                aux = list(cls.statesdict[state])
                for edge in cls.statesdict[state]:
                    aux.remove(edge)
                    if "-" in edge[1]:
                        for newedge in aux:
                            if matchindeterminacy(newedge[1],edge[1]):
                                aux.remove(newedge)

                    print aux


def random(self):
    """
    :param seed: Put a seed to generate random FSMs (default: "seed")
    :param min: The minimum number of inputs or outputs in the FMS (included)
    :param max: The maximum number of inputs or outputs in the FMS (included)
    :param states:
    :return: A pack of random FSMs
    """
    seed = self["seed"]
    inputs = self["input"]
    outputs = self["output"]
    states = self["states"]

    self["type"] = "random"

    statesdict = {}

    np.random.seed(int(seed, 36))
    npri = np.random.random_integers
    # numinput = npri(min, max)
    # numoutput = npri(min, max)
    numinput = inputs
    numoutput = outputs

    if "pattern" in self:
        numoutput = 1
    stateslist = ['s'+str(i) for i in range(states)]
    for state in stateslist:
        stl = []
        for premise in range(2**numinput):
            input = fix_size(bin(premise)[2:], numinput)
            o = npri(2**numoutput) - 1
            output = fix_size(bin(o)[2:], numoutput)
            nextstate = npri(stateslist.__len__()) - 1
            stl.append((stateslist[nextstate],input,output))
            statesdict[state] = stl

    # Calcular inaccesibilidad

    candidates = inaccess(statesdict, [], 0, {})

    if candidates.__len__() != statesdict.__len__():
        for i in range(statesdict.__len__()):
            if not candidates.has_key("s"+str(i)):
                for j in candidates:
                    if candidates[j].__len__() != 0:
                        initialState = candidates[j].pop()
                        edge = statesdict[initialState]
                        nlist = []
                        for k in edge:
                            if k[0] == j:
                                nlist.append(("s"+str(i), k[1],k[2]))
                            else :
                                nlist.append(k)
                        statesdict[initialState] = nlist

    return statesdict

def pattern(self):
    statesdict = {}
    patternlist = []
    input = self["input"]
    nPatterns = self["output"]
    seed = self["seed"]

    self["type"] = "pattern"

    np.random.seed(int(seed, 36))
    npri = np.random.random_integers

    allPatterns = getPatternList(self["states"], input)

    for i in range(nPatterns):
        if allPatterns.__len__() == 0:
            break
        patternlist.append(allPatterns.pop(npri(allPatterns.__len__()-1)))


    patternCont = 0
    self["patternlist"] = patternlist
    for i in patternlist:
        splitted = []
        cont = 0
        print i
        for j in range(i.__len__()/input):
            cont += input
            splitted.append(i[cont-input:cont])


        def createSD(statesdict, crumb, pattern, patternCont):
            currentState = crumb[crumb.__len__()-1]
            if not statesdict.has_key(currentState):
                statesdict[currentState] = []
            exists = False

            for i in statesdict[currentState]:
                if pattern[0] == i[1]:
                    exists = i[0]
                    break
            if not exists:
                o = "0"
                state = "s"+str(statesdict.__len__())
                inserted = False
                if pattern.__len__() == 1:
                    o = str(patternCont+1)
                    patternCont += 1
                    inserted = True
                statesdict[currentState].append((state,pattern[0],o))
                crumb.append(state)

                if not inserted:
                    createSD(statesdict, crumb, pattern[1:], patternCont)

            else :
                crumb.append(exists)
                createSD(statesdict, crumb, pattern[1:], patternCont)


        createSD(statesdict, ["s0"], splitted, patternCont)
        patternCont += 1


    self["statesdict"] = statesdict
    return statesdict

def sequential(self):
    try:
        seed = self["seed"]
        input = self["input"]
        output = self["output"]
        states = self["states"]
    except KeyError:
        print "You must input seed, number of inputs/outputs and states parameters"
        return 1

    self["type"] = "sequential"

    if not "loops" in self:
        self["loops"] = 0
    if not "jumps" in self:
        self["jumps"] = 0

    if 100 <= self["loops"] + self["jumps"]:
        tkMessageBox.showinfo("Error", "loops + jumps must be less than 100")
        return 1

    statesdict = {}
    np.random.seed(int(seed,36))
    npri = np.random.random_integers
    stateslist = ['s'+str(i) for i in range(states)]

    if (self["loops"] == 0) and (self["jumps"] == 0):
        i = 1
        for state in stateslist:
            o = npri(2**int(output)) - 1
            out = fix_size(bin(o)[2:], output)
            op = ""
            for l in range(input):
                op = op + "-"
            statesdict[state] = [(stateslist[i%(stateslist.__len__())],op,out)]
            i += 1
    else:

        i = 1
        for state in stateslist:
            res = []
            for inp in range(2**int(input)):
                out = npri(1,2**int(output)) - 1
                nextState = stateslist[i%(stateslist.__len__())]
                dice = npri(0,100)
                if dice < self["jumps"] :
                    myrandom = npri(0,stateslist.__len__()-1)
                    nextState = stateslist[myrandom]

                else:
                    if dice < (self["jumps"]+self["loops"]):
                        nextState = state


                res.append((nextState,fix_size("{0:b}".format(inp),input),fix_size("{0:b}".format(out),output)))

            statesdict[state] = res
            i += 1

        candidates = inaccess(statesdict, [], 0, {})

        if candidates.__len__() != statesdict.__len__():
            for i in range(statesdict.__len__()):
                if not candidates.has_key("s"+str(i)):
                    for j in candidates:
                        if candidates[j].__len__() != 0:
                            initialState = candidates[j].pop()
                            edge = statesdict[initialState]
                            nlist = []
                            for k in edge:
                                if k[0] == j:
                                    nlist.append(("s"+str(i), k[1],k[2]))
                                else :
                                    nlist.append(k)
                            statesdict[initialState] = nlist


        self["statesdict"] = statesdict



    return statesdict

