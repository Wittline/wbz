from operator import itemgetter

class Bwt:

    # rotations = list(obj.string_rotations(seq))
    # bwm = obj.construct_bwm(rotations[-1])
    # bwt_seq = obj.encode_bwt(bwm)

    # bwm = list(obj.reconstruct_bwm(bwt_seq))
    # original = obj.decode_bwt(bwm[-1])
    # original

    def __init__(self, fc):
        self.fc = fc

    def string_rotations(self, seq):

        seq += self.fc
        double_seq = seq * 2
        all_rotations = []

        for i in range(0, len(seq), 1):

            rot = double_seq[i:i+len(seq)]
            all_rotations.append(rot)

            yield [rot for rot in all_rotations]

    def construct_bwm(self, rotations):
        sorted_rotations = sorted(rotations)
        return sorted_rotations

    def encode_bwt(self, mat):

        last_column = []
        for line in mat:
            last_char = line[-1]
            last_column.append(last_char)

        transformed_seq = ''.join(last_column)
        return transformed_seq

    def reconstruct_bwm(self, bwt):

        bwm = []        
        for _ in range(0, len(bwt), 1):
            bwm.append('')

        for _ in range(0, len(bwt), 1):

            for i in range(0, len(bwt), 1):
                bwm[i] = bwt[i] + bwm[i]
 
            yield [line for line in bwm]
            bwm.sort()
            yield [line for line in bwm]

    def decode_bwt(self, mat):

        seq = ""
        for line in mat:
            if line[-1] == self.fc:
                seq += line

        return seq[:-1]

    # def decode(self, seq):
    #     bwm = list(self.reconstruct_bwm(seq))
    #     return self.decode_bwt(bwm[-1])

    def rankBwt(self, lastColumn):
        tots = dict()
        ranks = []
        for col in lastColumn:
            if not(col in tots):
                tots[col] = 0
            ranks.append(tots[col])
            tots[col] = tots[col] + 1
        return ranks, tots


    def firstColumn(self, tots):
        firstC = {}
        totc = 0
        for c, counter in sorted(tots.items()):
            firstC[c] = (totc, totc + counter)
            totc += counter
        return firstC    

    def decode(self, bwt):
        ranks, tots = self.rankBwt(bwt)
        first = self.firstColumn(tots)
        rowi = 0 # First row
        outputS = self.fc # Last char
        while bwt[rowi] != self.fc:
            c = bwt[rowi]
            outputS = c + outputS
            rowi = first[c][0] + ranks[rowi]
        return outputS    

    # def decode(self, s):

    #     I = s.index(self.fc)
    #     s.pop(I)
    #     n = len(s)
    #     X = sorted([(i, x) for i, x in enumerate(s)], key=itemgetter(1))
    #     T = [None] * n

    #     for i, y in enumerate(X):
    #         j, _ = y
    #         T[j] = i

    #     Tx = [I]
    #     for i in range(1, n):
    #         Tx.append(T[Tx[i-1]])

    #     S = [s[i] for i in Tx]

    #     S.reverse()        
    #     return S

        

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