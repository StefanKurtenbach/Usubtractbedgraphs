# Usubstractbedgraphs v2.6

import argparse
import sys
import os
from array import *

#get arguments from command line
parser = argparse.ArgumentParser(description='Uaveragebedgraphs_args')
parser.add_argument('-o','--output', help='name of output file', required=True, type=str)
parser.add_argument('-f1','--file1', help='file1', required=True, type=str)
parser.add_argument('-f2','--file2', help='file2', required=True, type=str)
parser.add_argument('-d','--delete', help='delete all overlap with file 2', required=False, type=str, default = "N")

args = vars(parser.parse_args())
file1 = args['file1']
file2 = args['file2']
output_file = args['output']
deleteall = args['delete']

try: os.remove(output_file)
except: pass

def substract (file1, file2, newfile):
# make list of chromosomes
    chromosomes = []
    files = [file1, file2]
    for file in files:
        with open(file) as f:
            for line in f:
                line_split = line.split("\t")
                if line_split[0] not in chromosomes:
                    chromosomes.append(line_split[0])

    done = "no"
    while done == "no":
        try:
            current_chromosome = chromosomes.pop(0)
        except:
            break

# get length of current chromosome
        stop = 0
        for file in files: # go through all files
            with open(file) as f:
                for line in f:
                    line_split = line.split("\t")
                    if line_split[0] == current_chromosome:
                        if int(line_split[2]) > stop:
                            stop = int(line_split[2])
        if stop > 0:  #continue only if values in chromosome
            output = array('f', [0] * stop)

#substract
            for x, file in enumerate(files):
                with open(file) as f:
                    for line in f:
                        line_split = line.split("\t")
                        line_split[3] = line_split[3].replace("\n", "")
                        if line_split[0] == current_chromosome:
                            if float(line_split[3]) > 0:
                                for o in range(int(line_split[2]) - int(line_split[1])):
                                    coord = o + int(line_split[1])
                                    if x == 0:
                                        output[coord] = float(line_split[3])
                                    elif x == 1:
                                        if deleteall == "N":
                                            output[coord] = output[coord] - float(line_split[3])
                                        elif deleteall == "Y":
                                            output[coord] = 0
                                        else:
                                            print("Error: -d has to be N or Y")
                                            sys.exit()

#concatenate entries with same value
            output2 = []
            temp_entry = []
            for x, value in enumerate(output):
                if value != 0:
                    if temp_entry == []:
                        temp_entry = [current_chromosome, x, x + 1, value]
                    elif temp_entry[3] == value:
                        temp_entry[2] += 1
                    elif temp_entry[3] != value:
                        output2.append(temp_entry)
                        temp_entry = [current_chromosome, x, x + 1, value]
                else: temp_entry == []

            if temp_entry != []:
                output2.append(temp_entry)

            print(output2)

            with open(newfile, "a") as f:
                for row in output2:
                    print("a")
                    f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\n")

############################################################################

substract(file1, file2, output_file)
print("Success :)")
