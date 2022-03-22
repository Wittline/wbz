
class BitsBytes:

    def __init__(self):
        pass

    def encode(self, sbits):
        return [int(sbits[i:i+8], 2) for i in range(0, len(sbits), 8)]