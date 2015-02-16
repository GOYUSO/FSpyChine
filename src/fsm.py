__author__ = 'Antonio Segura Cano'

import os
import re

# We'll create a FSMachine class
# FSMachine class will generate all methods about the program
# A random FSMachine: FSMachine.random

#     KISS2 headers include the following information:
#
#
#     .i  n    # number of inputs
#     .o  m    # number of outputs
#     .p  p    # number of products
#     .s  s    # number of states used


class FSMachine:
    """ Clase principal """
    def __init__(self,info):
        """
        :param info: it can be a file or a dictionary
        :return: FSMachine object
        """

    @staticmethod
    def random(entradas):
        """
        :param entradas:
        :return:
        """


# Util functions

def kiss2png(file):
    infile = open(file, 'r')
    outfile = open("./temp.txt",'a')
    outfile.write("digraph g{\n\t")
    metadata = {}
    nline = 1

    for line in infile:
        pattern = re.compile("^.[iops]")
        p = pattern.findall(line)
        chunksline = line.split()
        writeMem = ''
        if p:
            key = chunksline[0].replace(".","")
            val = chunksline[1]
            metadata[key]=val
        else:
            lenc = chunksline.__len__()
            if lenc != 4:
                if lenc == 0:
                    continue
                print "Format kiss2 wrong at line "+nline.__str__()+""
                os.system('(date "+DATE: %Y-%m-%d%nTIME: %H:%M" && echo "'+file+' wrong at line '+nline.__str__()+'") >> ../logs/error.log')
                break
            else:
                if not (treatment_size(chunksline[0],metadata["i"]) and
                treatment_size(chunksline[3],metadata["o"])):
                    print "Error"
                else:
                    writeMem+=chunksline[1]+'->'+chunksline[2]+' [label="'+chunksline[0]+' '+chunksline[3]+'"];\n\t'
                    outfile.write(writeMem)

        nline+=1

    outfile.write("\r}")
    infile.close()
    outfile.close()
    os.system("dot temp.txt -o result.png -Tpng && rm temp.txt")


def treatment_size(str, len):
    return str.__len__() == int(len)

def log(type,line=False):
    return None



#print "Debug mode"
kiss2png("../res/testkiss2.txt")


