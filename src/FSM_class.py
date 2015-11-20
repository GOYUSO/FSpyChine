__author__ = 'Antonio Segura Cano'

import numpy as np
import time

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

    def kiss2(self):
        stated = self.statesdict
        name = time.strftime("FSM_%m%d%H%M%S.kiss2")
        if stated.__len__() != 0:
            p = 0
            i = False
            o = False
            outfile = open("./"+name, 'a')
            blob = ""
            for statenode in stated:
                if not i or not o or not r:
                    i = stated[statenode][0][1].__len__()
                    o = stated[statenode][0][2].__len__()
                    r = statenode
                for transition in stated[statenode]:
                    blob += transition[1] + " " + statenode + " " + transition[0] + " " + transition[2] + "\n"
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

    def image(self):
        infile = self.statesdict
        # outfile = open("./temp.txt", 'w').close()
        outfile = open("./temp.txt", 'w')
        outfile.write("digraph g{\n\t")
        writemem = ''

        for state in infile:
            for edge in infile[state]:
                writemem += state + ' -> ' + edge[0] + \
                            ' [label="' + edge[1] + ' ' + edge[2] + '"];\n\t'
        outfile.write(writemem+"\r}")
        outfile.close()

        os.system("dot temp.txt -o result.png -Tpng && rm temp.txt")

    def getPatterns(self):
        patternlist = []
        if "pattern" in self.meta:
            patternlist = getPatternsAux(self.meta["statesdict"],"s0",[],"")
        else:
            print "Method only allowed with pattern FSM"

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
    min = self["min"]
    max = self["max"]
    states = self["states"]

    statesdict = {}

    np.random.seed(int(seed, 36))
    npri = np.random.random_integers
    numinput = npri(min, max)
    numoutput = npri(min, max)

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
            print input + ' ' + state + ' ' + stateslist[nextstate] + ' ' + output
            stl.append((stateslist[nextstate],input,output))
            statesdict[state] = stl

    return statesdict

def pattern(self):
    self["min"] = self["input"]
    self["max"] = self["input"]
    self["pattern"] = True
    self["statesdict"] = random(self)

def sequential(self):
    try:
        seed = self["seed"]
        input = self["input"]
        output = self["output"]
        states = self["states"]
    except KeyError:
        print "You must input seed, number of inputs/outputs and states parameters"
        return

    statesdict = {}
    np.random.seed(int(seed,36))
    npri = np.random.random_integers
    stateslist = ['s'+str(i) for i in range(states)]

    if "loops" not in self or self["loops"] == 0:
        i = 1
        for state in stateslist:
            o = npri(2**int(output)) - 1
            out = fix_size(bin(o)[2:], output)
            statesdict[state] = [(stateslist[i%(stateslist.__len__())],"---",out)]
            i += 1
    else:

        i = 1
        for state in stateslist:
            res = []
            for inp in range(2**int(input)):
                out = npri(1,2**int(output)) - 1
                nextState = stateslist[i%(stateslist.__len__())]
                if npri(0,100) < self["loops"]*100 :
                    nextState = state

                res.append((nextState,fix_size("{0:b}".format(inp),input),fix_size("{0:b}".format(out),output)))

            statesdict[state] = res
            i += 1


        self["statesdict"] = statesdict



    return statesdict

# x = FSM(seed="prueba", min=1,max=4,states=4,indeterminacy=0.3)
# x.build(random)

x1 = FSM(seed="mySeed", input=3, output=2, states=5, loops=0.5)
x1.build(pattern)
x1.image()
x1.getPatterns()
