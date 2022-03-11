from operator import itemgetter

class Bwt(object):

    def __init__(self, fc):
        # mark character
        self.fc = fc

    def encode(self,s):  
        n = len(s)
        m = sorted([s[i:n]+s[0:i] for i in range(n)])
        I = m.index(s)
        L = [q[-1] for q in m]
        L = L[:]
        L[I:I] = [self.fc]
        return L


    def decode(self, s):

        I = s.index(self.fc)
        s.pop(I)

        n = len(s)
        X = sorted([(i, x) for i, x in enumerate(s)], key=itemgetter(1))

        T = [None] * n
        for i, y in enumerate(X):
            j, _ = y
            T[j] = i

        Tx = [I]
        for i in range(1, n):
            Tx.append(T[Tx[i-1]])

        S = [s[i] for i in Tx]
        S.reverse()
        return S
