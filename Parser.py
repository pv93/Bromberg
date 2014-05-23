import argparse
import os.path
import dictbuild

parser = argparse.ArgumentParser("This is the big kahuna. No more games")
parser.add_argument('-p', '--ptt', help = 'The ptt file(s) to be used', nargs = '*')
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

iteration = args.iter

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



    
