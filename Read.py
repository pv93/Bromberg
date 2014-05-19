import Gene

"""
By Pavel Vaysberg
Updated: 4/8/2014
pvaysberg@gmail.com
"""

class Read:

    name = None #R_n
    start, finish = 0, 0 #Start and end positions on genome, may make this a string "s-f"
    numOfGenes = 0 #int, will use as size of list for genes
    genelist = [] #list of genes
    subseq = None #subsequence
    
    def __init__(self, num, start, finish): # find out default init, may want to unload this one
        self.name = "R_" + str(num)
        self.start = start
        self.finish = finish
        self.subseq = ""
        self.genelist = []
        self.numOfGenes = 0

    def getsubsequence(self, sequence): 

        self.subseq = sequence[self.start-1:self.finish]

    def annotate(self, pttFile, sequence):
        
        proteinFile = open(pttFile, 'r')
        
        

        with proteinFile as f:
            for i in xrange(3): #skip the header lines, go directly to data. Restricts to ptt file, is there a better way?
                f.next()
            
            for line in f:
                self.getsubsequence(sequence)
                
                cols = line.split('\t')
                geneRange = cols[0]
                
                getNums = geneRange.split("..")
                gbegin = int(getNums[0])
                gend = int(getNums[1])

                
                if ((gend < self.start) or (gbegin > self.finish)): #gene is not in read or...
                    if gbegin > self.finish:
                        break
                    else:
                        continue

                self.numOfGenes += 1 #...we found a gene. yay!
                geneName = cols[4]
                geneStrand = cols[1]
                readStart, readEnd = 0, 0

                if ( (self.start < gbegin) and (self.finish > gend ) ): # check to see if gene is entirely contained in read (up to NOT including ends) --[--####---]--
                    readStart, readEnd = (gbegin - self.start), (gend - self.start)
                    
                    
                elif ( (self.start > gbegin) and (self.finish > gend) ): # check to see if beginning of read intercepts a gene (but not end) ###[###------]---
                    readStart, readEnd = 1, (gend - self.start)
                    

                elif ( (self.start < gbegin) and (self.finish < gend) ): # check to see if end of read intercepets a gene (but not beginning) ---[----###]###
                    readStart, readEnd = (gbegin - self.start), len(self.subseq)
                    

                else: #this means that the gene is completely contained in the read (inclusive) or that the gene is larger than the read and spans the entire thing -###[#####]##--
                    readStart, readEnd = 1, len(self.subseq)

                gene = Gene.Gene(geneName, geneStrand, readStart, readEnd)
                self.genelist.append(gene)
        proteinFile.close()
