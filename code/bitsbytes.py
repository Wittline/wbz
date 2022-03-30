import time
class BitsBytes:

    def __init__(self):
        pass

    def encode(self, bi):          
        return [int(bi[i:i+8], 2) for i in range(0, len(bi), 8)]

    def decode(self, by):        
        return [''.join(format(b, "08b") for  b in by)]