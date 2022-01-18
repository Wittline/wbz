class Bwt:

    def __init__(self, sc, fc):
        # space character
        self.sc = sc
        # mark character
        self.fc = fc
        

    def __fix_str(self, str):
        str = str.replace(' ', self.sc)
        return str + self.fc

    def __sa(self, s):
        st = sorted([(s[x:], x) for x in range(0, len(s))])
        return map(lambda x: x[1], st)

    def __rank(self, bw):
        ts = dict()
        rks = []
        for c in bw:
            if c not in ts:
                ts[c] = 0
            rks.append(ts[c])
            ts[c] += 1
        return rks, ts

    def __fc(self, ts):
        first = {}
        tc = 0
        for c, count in sorted(ts.items()):
            first[c] = (tc, tc + count)
            tc += count
        return first      

    def encode(self, str):

        str = self.__fix_str(str)

        bw = []
        for i in self.__sa(str):
            if i == 0:
                bw.append(self.fc)
            else:
                bw.append(str[i-1])

        outstr = ''.join(bw)

        print(str, "<------->", outstr)

        return outstr
    
    def decode(self, bw):
        rks, ts = self.__rank(bw)
        first = self.__fc(ts)
        ri = 0
        t = self.fc
        while bw[ri] != self.fc:
            c = bw[ri]
            t = c + t            
            ri = first[c][0] + rks[ri]

        t = t.replace(self.sc, ' ')
        return t[0:-1]
