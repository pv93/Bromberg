class dictbuild:

    piddict = {}
    cogdict = {}

    
    # this method will build 2 dictionaries. One that relates PID -> COG_ID
    # and one that keeps track of how many times a cog id shows up
    def build(self, pttfile): 

       proteinfile = open(pttfile, 'r')

       with proteinfile as f:
            for i in xrange(3): #skips first 3 lines, only works if all ptt files are exactly identical in format... assuming that they do, though that could be reckless
                f.next()
            for line in f:
                cols = line.split('\t')
                if not cols[7] == '-':       # if a gene has no cogid, it's not useful to us... right?

                    self.piddict[cols[3]] = cols[7] # entry in piddict {PID : COG_ID}

                    if cols[7] not in self.cogdict: #entry in cogdict {COG_ID : number of occurences}
                        self.cogdict[cols[7]] = 1
                    else:
                        self.cogdict[cols[7]] += 1
                        
       proteinfile.close()
        

