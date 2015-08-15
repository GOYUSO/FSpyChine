__author__ = 'Antonio Segura Cano'

import os
import re
import numpy as np
import time

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

    def fsm2image(self, *filepath):
        if self.statesdict.__len__() != 0:
            pass #TODO-fsm2image
        else:
            print "Sorry, but you must create a FSM with 'built' method first"

    def build(self, f):
        self.statesdict = f(self.meta)
        ind, loops = 0,0
        if self.meta.has_key("indeterminacy"):
            ind = self.meta['indeterminacy']
        if ind != 0 and ind < 1 and 0 < ind:
            self.__makeindeterminacy(ind)

        if self.meta.has_key("loops"):
            loops = self.meta.loops
        if loops != 0 and loops < 1 and 0 < loops:
            self.__makeloops(loops)


    def kiss2(self):
        stated = self.statesdict
        name = time.strftime("FSM_%m%d%H%M%S.kiss2")
        if(stated.__len__() != 0):
            p = 0
            i,o = False, False
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

    def kiss2png(self):
        infile = self.statesdict
        # outfile = open("./temp.txt", 'w').close()
        outfile = open("./temp.txt", 'w')
        outfile.write("digraph g{\n\t")
        writemem = ''

        for state in infile:
            for edge in infile[state]:
                writemem += state + '->' + edge[0] + \
                            ' [label="' + edge[1] + ' ' + edge[2] + '"];\n\t'
        outfile.write(writemem+"\r}")
        outfile.close()

        os.system("dot temp.txt -o result.png -Tpng && rm temp.txt")


    def __makeindeterminacy(self, *args):
        # TODO - makeindeterminacy private method
        if args:
            ind = args[0]*100
            npri = np.random.random_integers

            for state in self.statesdict:
                statesdict = list(self.statesdict)
                for edge in self.statesdict[state]:
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


    def __makeloops(self, *args):
        if args:
            pass #TODO- makeloops private method


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
    pass #TODO pattern

def sequential(self):
    pass #TODO sequential

x = FSM(seed="prueba", min=2,max=4,states=6,indeterminacy=0.3)
x.build(random)
x.kiss2png()

print "Para"

