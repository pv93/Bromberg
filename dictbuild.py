#import cPickle as pickle
import marshal
import argparse
import os, os.path


# This module will take a .ptt file as input, and generate a dictionary and a list. These dictionaries will then be saved as files ('pickled') to be used in the Parser.py script
# The dictionaries are: { PID : COG } - for associating PID's with COGs
#                       [1 seq cogs] - we use this list to make sure that we are excluding all PIDS with only one cog, in order to add them to our FN list






# TO DO
# Make a destination script





parser = argparse.ArgumentParser("Builds dictionaries to be used in Parser program")
parser.add_argument('-p', '--ptt', help = 'The ptt file(s) to be used, can also input a directory', nargs = '*')

args = parser.parse_args()
pttfiles = args.ptt
if not pttfiles:
    pttfiles = []
    while True:
        x = raw_input("You have not entered any .ptt files! Enter here, one by one. Press 'q' to stop: ")
        if x == 'q' and len(pttfiles) == 0:
            continue
        elif x == 'q':
            break
        else:
            pttfiles.append(x)

for index, dircheck in enumerate(pttfiles): # checking if the user input a directory for the -p option, note that they could use a combination
    if os.path.isdir(dircheck):
        for files in os.listdir(dircheck):
            if files[-4:] == '.ptt':
                abspath = os.path.abspath(dircheck + "//" + files)
                pttfiles.append(abspath)            
        del pttfiles[index]


cogdict = {}

for pttfile in pttfiles:
    proteinfile = open(pttfile, 'r')

    with proteinfile as f:
        for i in xrange(3):                     # skips first 3 lines, since they are the header of a .ptt file
            f.next()
        for line in f:
            cols = line.split('\t')
            if not cols[7] == '-':              # cols[7] is the COG, cols[3] is PID
                if cols[7] not in cogdict:
                    cogdict[cols[7]] = [cols[3]]
                else:
                    cogdict[cols[7]].append(cols[3]) # building a dictionary of { COG : [PID's] }
    proteinfile.close()


piddict = {}
for cog in cogdict:
    if len(cogdict[cog]) > 1:
        for pid in cogdict[cog]:
            piddict[pid] = cog
            
            

with open("pidcog.pickle", 'wb') as handle:
    marshal.dump(piddict, handle)

handle.close()

