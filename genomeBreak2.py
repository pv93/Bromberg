import random
import Read
import argparse
import os

""" This script will take a .fna file and a .ptt file as input, break
the sequence in the .fna file into random reads of length 50-250, and
return an output file that gives the reads, annotated using the
information given in the .ptt file

by Pavel Vaysberg
pvaysberg@gmail.com
Last updated: 4/8/2014 """


parser = argparse.ArgumentParser('This script will take a .fna file and a .ptt file as input, break the sequence in the .fna file into random reads of length 50-250, and return an output file that gives the reads, annotated using the information given in the .ptt file. If command line arguments are not used, user will be prompted after running the script.')
parser.add_argument('-f', '--fna', help = "The fna file to be used")
parser.add_argument('-p', '--ptt', help = "The ptt file to be used")
parser.add_argument('-n', '--num', type = int, help = "Desired number of reads")

args = parser.parse_args()
seq_in = args.fna
ptt_in = args.ptt
num = args.num


def breakSequence(sequence, numOfReads, minSize, maxSize, outputfilename): 
    
    reads = [] 
    start, finish = 0, 0
    count = 1
    output = open(outputfilename, 'w')
    
    while (count <= numOfReads):

        start = random.randint(1, len(sequence))
        if (start + 50) > len(sequence):
            start = start - 50 #perhaps a better way to handle this?
        finish = start + random.randint(50,250)

        read = Read.Read(count, start, finish)
        read.annotate(ptt_in, sequence)
        reads.append(read)

        count += 1
        if count%10 == 0: # write to file every time size(reads) gets to 10
            for x in reads:
                if x.numOfGenes == 0: bar = ''
                else: bar = '|' # so that an extra '|' is not shown if there are 0 genes
                output.write( '> ' + x.name + '|' + str(x.start) + '-' + str(x.finish) + '|' + str(x.numOfGenes) + bar + '|'.join(map(str, x.genelist)) + '\n' + x.subseq + '\n' + '\n')
            del reads[:]
    output.close()
            
    
            

# Read input from file

if not seq_in:
    seq_in = raw_input("Enter a sequence file: ") 

if not ptt_in:   
    ptt_in = raw_input("Enter a .ptt file: ")

if not num:
    num = input("Enter desired number of reads: ")

rawseqfile = open(seq_in, 'r')
lines = rawseqfile.readlines()

# Making one long DNA sequence, no newlines or headers
sequence = ""
for line in lines:
    if '>' in line:
        continue
    else:
        sequence = sequence + line

rawseqfile.close()
sequence = sequence.replace('\n', '') # can also use line = line.rstrip() on each line. Which is better, all at once or line by line?

#output into a file
seq_in = seq_in.replace(".txt", '') #in case user inputs .txt at the end e.g. NC_12345.fna.txt
name = seq_in[:-4]
outputfilename = name + ".rds" 

breakSequence(sequence, num, 50, 250, outputfilename)
