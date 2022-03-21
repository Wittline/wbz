class Mtf:

    def __init__(self):
        self.table = []
        for i in range(256):
            self.table.append(chr(i))
    
    def encode(self, str):
       
        seq, pad = [], self.table[::]
        for cr in str:
            inx = pad.index(cr)
            seq.append(inx)
            pad = [pad.pop(inx)] + pad
       
        return seq
        

    def decode(self, seq):
        chrs, pad = [], self.table[::]
        for inx in seq:
            chr = pad[inx]
            chrs.append(chr)
            pad = [pad.pop(inx)] + pad
        return chrs

