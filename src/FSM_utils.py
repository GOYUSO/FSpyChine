__author__ = 'Antonio Segura Cano'
__name__ = 'utils'

import os
import math

import tkMessageBox

def fix_size(s, l):
    r = s
    if s.__len__() != l:
        r = fix_size("0"+s, l)
    return r


def hasindeterminacy(edge):
    res = False
    if '-' in edge[1]:
        res = True
    return res


def matchindeterminacy(s0, s1):
    res = True
    for bit0, bit1 in zip(s0, s1):
        if bit0 != '-' and bit0 != bit1:
            res = False
            break
    return res


def log(filepath, numline):
    print "Format kiss2 wrong at line " + numline.__str__()
    os.system('(date "+DATE: %Y-%m-%d%nTIME: %H:%M" && echo "' + filepath +
              ' wrong at line '+numline.__str__() + '") >> ../logs/error.log')


def treatment_size(s, l):
    return s.__len__() == int(l)

def getPatternsAux(statesdict, actual, statesvisited, value0):
    state = statesdict[actual]
    value = value0
    statesvisited.append(actual)
    store = ""
    for edge in state:
        value += edge[1]
        if edge[0] in statesvisited:
            return
        if edge[2] == "1":
            statesvisited.append(edge[1])
            store += store +"\n"+ value
        else:
            getPatternsAux(statesdict, edge[0], statesvisited, value)

    tkMessageBox.showinfo("The patterns are the following: ",store)


