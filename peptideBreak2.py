import argparse
import re
import Gene

"""" This script will take a .rds file and translate every read. It will then
return all amino acid sequences of length >= 11. AA sequences are broken up
first by reading frame, then by stop codon.

By Pavel Vaysberg
pvaysberg@gmail.com
Last updated: 4/9/14
"""

parser = argparse.ArgumentParser("""This script will take an .rds file and translate the sequences within.
                         It will return an output file containing all peptides of length >= 11""")
parser.add_argument('-r', '--rds', help = "The .rds file you'd like to translate")
args = parser.parse_args()
rdsfile = args.rds

if not rdsfile:
    rdsfile = raw_input("Enter an .rds file: ")

# DNA codon table
bases = ['T', 'C', 'A', 'G']
codons = [a+b+c for a in bases for b in bases for c in bases]
amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
codon_table = dict(zip(codons, amino_acids))


# Function to translate a DNA sequence, looking at all 6 reading frames
# Will return a list of all AA sequences >= 11, separated by stop codons

class Peptide:
    chain = ""
    genes = []

    def __init__(self, chain):
        self.chain = str(chain)
        self.genes = []
    def addgene(self, gene):
        self.genes.append(gene)
        return
    def getgenenames(self): 
        names = []
        for gene in self.genes:
            names.append(gene.name)
        return names

def replace(sequence):
    temp = ""
    for x in sequence:

        if x == 'A' :
            temp += 'T'
            continue
        if x == 'T' :
            temp += 'A'
            continue
        if x == 'C' :
            temp += 'G'
            continue
        if x == 'G' :
            temp += 'C'
            continue
    newsequence = temp
    return newsequence


def translate(sequence, genes):

    
    peptidelist = [] # return value
    
    for s in range(0,2): # 2 strands
        for n in range(0,3): #  3 reading frames
            
            sequence1 = sequence.strip()
    
            if s == 1:
                sequence1 = replace(sequence1[::-1])
                
            presequence = ""
            for c in range(0,len(sequence),3):

                codon = sequence1[c+n:(c+n)+3]
                if len(codon) < 3: #we've reached the end
                    break



                presequence = presequence + codon_table[codon] # building our peptide sequence


            fraglist = presequence.split('*')
            
            pointer = 1 # this pointer tracks the location in the gene that our slices of AA sequences correspond to
            
            for x in fraglist: # assign genes to each peptide
                
                if len(x) < 11:
                    if x == '': pointer += 1 # this accounts for multiple stop codons
                    pointer += len(x)
                    continue
                else:
                    peptide = Peptide(x)

                if not pointer == 1: pointer += 1 # accounting for stop codon

                for gene in genes:
                    if ((gene.strand == '+' and s == 1) or (gene.strand == '-' and s == 0)): # gene is in opposite strand, don't need it
                           continue

                    pepstart = 1 + 3*(pointer-1)
                    pepend = (pointer + len(x))*3
                    
                    if (s == 1 and gene.strand == '-'): # looking for gene on opposite strand
                        mstrand_start = len(sequence1) - gene.locOnReadEnd
                        mstrand_end = len(sequence1) - gene.locOnReadStart

                        if ((( pepstart + n ) > mstrand_end) or ( pepend + n < mstrand_start)): # checks if the amino acid sequence is NOT in range of the gene
                            continue
                        else:
                            peptide.addgene(gene)
                        
                    elif ((( pepstart + n ) > gene.locOnReadEnd) or ( pepend + n < gene.locOnReadStart)): # checks if the amino acid sequence is NOT in range of the gene
                        continue
                    else:
                        peptide.addgene(gene)
                       

                pointer += len(x)
                peptidelist.append(peptide)
    return peptidelist

name = rdsfile.replace('.txt','')
name = name[:-4]
outfile = open(name + '.prd', 'w')
with open(rdsfile, 'r') as reads:
    for line in reads:
        if '>' in line:
           header = line.replace('\n', '')
           header = header.replace('>', '')
           header = header.replace(' ', '')

           readline = header.split(',')
       
           sequence = next(reads) 

           genes = []
           
           for n in range(3,len(readline)-1,3):
                locsonread = readline[n+2].split('-')
                
                genes.append(Gene.Gene(readline[n], readline[n+1], int(locsonread[0]), int(locsonread[1])))


           peptides = translate(sequence, genes)
           count = 1
           for peptide in peptides:
              
               outfile.write('> ' + readline[0] + ', ' + 'P_' + str(count) + ', ' + ', '.join(map(str, peptide.getgenenames())) + '\n' + peptide.chain + '\n\n')
               count += 1
outfile.close()
reads.close()
