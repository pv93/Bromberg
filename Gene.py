class Gene:

    name = None
    strand = None
    locOnReadStart = 0
    locOnReadEnd = 0


    def __init__(self, name, strand, locOnReadStart, locOnReadEnd):

        self.name = name
        self.strand = strand
        self.locOnReadStart = locOnReadStart
        self.locOnReadEnd = locOnReadEnd

    def __str__(self):
        return self.name + ", " + self.strand + ", " + str(self.locOnReadStart) + " - " + str(self.locOnReadEnd)

    def __repr__(self):
        return self.name + ", " + self.strand + ", " + str(self.locOnReadStart) + " - " + str(self.locOnReadEnd)
        
