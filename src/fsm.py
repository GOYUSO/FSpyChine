__author__ = 'Antonio Segura Cano'

import os
import re
import numpy as np

# We'll create a FSMachine class
# FSMachine class will generate all methods about the program
# A random FSMachine: FSMachine.random

#     KISS2 headers include the following information:
#
#     .i    # number of inputs
#     .o    # number of outputs
#     .p    # number of products
#     .s    # number of states used
#     .r    # RESET state


class FSMachine:
    """ FSMachine class """
    def __init__(self, n=10):
        """
        :param n: Number of Final State Machines that you want to create at the package (default: 10)
        :return: FSMachine package ready to work with it.
        """
        self.n = n

    def random(self, seed="seed", min=1, max=8, states=10):
        """
        :param seed: Introduce a seed to generate random FSMs (default: "seed")
        :param min: The minimum number of inputs or outputs in the FMS (included)
        :param max: The maximum number of inputs or outputs in the FMS (included)
        :param states:
        :return: A pack of random FSMs
        """
        np.random.seed(int(seed, 36))
        npri = np.random.random_integers
        for fsm in range(self.n):
            numinput = npri(min, max)
            numoutput = npri(min, max)
            stateslist = ['s'+str(i) for i in range(states)]
            for state in stateslist:
                for premise in range(2**numinput):
                    input = fix_size(bin(premise)[2:], numinput)
                    o = npri(2**numoutput) - 1
                    output = fix_size(bin(o)[2:], numoutput)
                    nextstate = npri(stateslist.__len__()) - 1
                    print input + ' ' + state + ' ' + stateslist[nextstate] + ' ' + output


# Util functions
def kiss2png(filepath):
    infile = open(filepath, 'r')
    outfile = open("./temp.txt", 'a')
    outfile.write("digraph g{\n\t")
    metadata = {}
    nline = 1

    for line in infile:
        pattern = re.compile("^.[ioprs]")
        p = pattern.findall(line)
        chunksline = line.split()
        writemem = ''
        if p:
            key = chunksline[0].replace(".", "")
            val = chunksline[1]
            metadata[key] = val
        else:
            lenc = chunksline.__len__()
            if lenc != 4:
                if lenc == 0:
                    continue
                log(filepath, nline)
                break
            else:
                if not (treatment_size(chunksline[0], metadata["i"]) and treatment_size(chunksline[3], metadata["o"])):
                    log(filepath, nline)
                    break
                else:
                    writemem += chunksline[1]+'->'+chunksline[2]+' [label="'+chunksline[0]+' '+chunksline[3]+'"];\n\t'
                    outfile.write(writemem)
        nline += 1
    outfile.write("\r}")
    infile.close()
    outfile.close()
    os.system("dot temp.txt -o result.png -Tpng && rm temp.txt")


def treatment_size(s, l):
    return s.__len__() == int(l)


def fix_size(s, l):
    r = s
    if s.__len__() != l:
        r = fix_size("0"+s, l)
    return r


def log(filepath, numline):
    print "Format kiss2 wrong at line " + numline.__str__() + ""
    os.system('(date "+DATE: %Y-%m-%d%nTIME: %H:%M" && echo "' +
              filepath + ' wrong at line '+numline.__str__() + '") >> ../logs/error.log')


def wild_state(s1, s2):
    n, i = 0, 0
    r = True
    for letter in s1:
        if letter != s2[i]:
            n += 1
            if 1 < n:
                r = False
                break
        i += 1
    if n == 0:
        r = False
    print r

wild_state("0010", "0110")

# FSMachine(1).random()
# print "Debug mode"
# kiss2png("../res/testkiss2.kiss2")

# r opcional
# sino esta r -> primer estado
#
# random -> el rango de entradas va de [n,m] uniforme
# 	valor de campana mu y sigma
# mu, sigma = 0, 0.1 # mean and standard deviation
# >>> s = np.random.normal(mu, sigma, 1000)
#
# completamente especificada
# inespecificada (representacion)

#
# coherencia a la hora de escribir un kiss2