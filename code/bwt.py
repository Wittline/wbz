from operator import itemgetter

class BWT:

    def __init__(self, fc):
        self.fc = fc        

    def decode(self, seq):

        I = seq.index(self.fc)

        n = len(seq)
        index_chars = sorted([(i, c) for i, c in enumerate(seq)], key=itemgetter(1))
        
        T = [None for i in range(n)]

        for i, c in enumerate(index_chars):
            j, _ = c
            T[j] = i

        Tx = [I]
        for i in range(1, n):
            Tx.append(T[Tx[i-1]])

        S = [ord(seq[i]) for i in Tx]
        
        return S[::-1][:-1]
        

    def suffix_array(self, seq):

        seq += self.fc
        suff_arr = []
        for i in range(0, len(seq), 1):
            suff_arr.append((seq[i:], i))

        return sorted(suff_arr)

    def encode(self, seq):

        bwt = []
        for suff in self.suffix_array(seq):
            i = suff[1]
            if i == 0:
                bwt.append(self.fc)
            else:
                bwt.append(seq[i - 1])

        return ''.join(bwt)