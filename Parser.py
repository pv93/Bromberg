import argparse
import os, os.path
#import cPickle as pickle
import marshal
import re

parser = argparse.ArgumentParser("Parser used to scan .out files")
parser.add_argument('-p', '--pcd', help = 'The { PID : COG } dictionary used to build the { PID : COG } dictionary, must be in .pickle format')
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

pickledcogdict = args.pcd

if not pickledcogdict:
    pickledcogdict = raw_input('Enter a dictionary file: ')

# Opening the PID : COG dictionary
with open(pickledcogdict, 'rb') as handle: 
    cogdict = marshal.load(handle)

fp2count = 0 # FALSE POSITIVE 2 | BLAST result with : no query PID/no self hit, hits subject, that has a COG
fp2file = open(outfile + " false positives 2.txt", 'w') # These results will be output into a file. Note that we are assuming that a gene with no PID is the same thing as a gene with a PID that doesn't hit itself

tn1count = 0 # TRUE NEGATIVE 1 | BLAST result with : no query PID/no self hit, hits subject, that does NOT have a COG

tn2count = 0 # TRUE NEGATIVE 2 | BLAST result with : no query PID / no self hit, hits nothing

tpcount = 0 # TRUE POSITIVE |  query has PID, query has COG, hits subject PID, with ~SAME~ COG
tpfile = open(outfile + " true positives.txt", 'w')

fp1count = 0 # FALSE POSITIVE 1 | query has PID, query has COG, hits subject PID, with ~DIFFERENT~ COG
fp1file = open(outfile + " false positives 1.txt", 'w')

testset = open(outfile + " test set.txt", 'w') # TEST SET | query has PID, query has COG, hits subject PID, with ~NO~ COG 
                                               # OR         query has PID, query has no COG, hits PID

fncount = 0 # FALSE NEGATIVE | query has PID, query has COG, hits nothing

uneg = 0 # UNCERTAIN NEGATIVES | query has PID, query has no COG, hits nothing


def self_hit_check(pid, hits):
    for hit in hits:
        split1 = hit.split('\t')
        hit_pid = split1[1].split('|')
        hit_pid = hit_pid[1]
        
        if pid == hit_pid:
            return True
    return False

def evaluate_hits(query, list_of_hits, dictionary):

    pids = query[2:]
    if len(pids) == 0:
        nopid = True

    else:

        for pid in pids:
            self_hit = self_hit_check(pid, list_of_hits)
            
        
    
    
    



# Parsing, note that this method is extremely dependent on the format of the outfile,
# something that should be addressed in future releases
with open(outfile, 'r') as ofile:
    

       # Parsing begins ... abandon hope all ye who enter
    
    rfile = ofile.readlines()
    for i, line in enumerate(rfile):
        
        your_iter = args.iter
        if "Iteration" in line: #ugh
            print "iteration in line \n" ################################3

            given_iter = int(re.findall('\d+', line)[0])
            print "given iteration is:", str(given_iter)

            j = i

            if (your_iter == 1 and given_iter > 1) or (your_iter > 1 and given_iter > 1): # We ignore the case when you want the first iteration and are on the 2nd,3rd... (since later iterations are useless)
                print "belee me" ##############################################
                continue                                                                  # Also ignore when we are looking for the last iteration and are not on the first, since the case where we get the last iteration is in the third if statement, and is implemented by starting with the first iteration
            
            # We're left with 2 situations : either you want the first iteration and are on it, or you want the last and are on the first

            elif (your_iter == 1 and given_iter == 1):

                while "hits found" not in rfile[j]: 
                    j += 1
                print "We're on iteration one : " + str(given_iter) ########################################
                print '\n' + str(rfile[j])####################################
                
            elif your_iter > 1 and given_iter == 1:

                while "Search has CONVERGED!" not in rfile[j]: # this will take us to the end of the last iteration
                    j += 1
                while "hits found" not in rfile[j]: # this will take us back to the beginning of the last iteration, so that we can grab all of the hits
                    j -= 1

                print "We're on last iteration : " + str(given_iter) ########################3
                print '\n' + str(rfile[j]) ###############################

            query = rfile[i+1].strip('# Query: ').split(',') # Will have to change split from ',' to '|'
            hits = []
            
            num = int(re.findall('\d+', rfile[j])[0]) # number of hits
            for x in xrange(j+1, j+num+1):
                hits.append(rfile[x])

            for hit in hits: ############################
                split1 = hit.split('\t') ############################
                if len(split1) > 1: # why is this necessary?                                    <---- use this in self_hit_check
                    hit_pid = split1[1].split('|') ############################
                    hit_pid = hit_pid[1] ############################

                print str(hit_pid)############################
            #evaluate_hits(query, hits, cogdict)

ofile.close()



##    for key in cogdict:
##        for pid in cogdict[key]:
##            
##
##    with readout as open(outfile, 'r'):
##        for line in readout:
##            if line.startswith('#'):



#while not pickledcogdict[-7:] == '.pickle':
 #   pickledcogdict = raw_input('Cog dictionary must be pickled! Enter a file that ends in .pickle, and is a valid serialized file')
