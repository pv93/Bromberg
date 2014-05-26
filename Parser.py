import argparse
import os, os.path
import dictbuild

parser = argparse.ArgumentParser("Parser used to scan .ptt and .out files")
parser.add_argument('-p', '--ptt', help = 'The ptt file(s) to be used, can also input a directory', nargs = '*')
parser.add_argument('-o', '--out', help = 'The .out file to be used')
parser.add_argument('-d', '--dest', help = 'Destination of output files')
parser.add_argument('-i', '--iter', type = int, default= 1, help ="Iteration of psi-blast to use")

# Parsing command line arguments
args = parser.parse_args()
if args.dest:
    save_path = args.dest

outfile = args.out
if not outfile:
    outfile = raw_input('Enter the .out file to be used: ')

pttfiles = args.ptt

if not pttfiles:
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

# Building our lovely dictionaries
dicts = dictbuild.dictbuild()

for files in pttfiles:
    dicts.build(files)

pid = dicts.piddict # { PID : COG_ID }
cog = dicts.cogdict # { COG_ID : # of occurences }

print pid, cog
count = 0
for keys in cog:
    if cog[keys] == 1:
        count += 1
print "Number of COGS with one associated gene: " + str(count)



    
