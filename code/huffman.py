from collections import Counter
from operator import length_hint
import timeit as tiempo

class NodeT:
    
    def __init__(self, freq, left, right, isLeaf, value):
         self.freq = freq
         self.left = left
         self.right = right
         self.isLeaf = isLeaf
         self.value = value            

class Huffman:

    def __init__(self):
        self.hufftable = {}
        self.codes = []
        self.tf = {}

    def _huffmanCodes(self, tl):
        if tl.isLeaf == False:
            l = tl.left
            r = tl.right
            self.codes.append("0")
            self._huffmanCodes(l)
            self.codes.pop()
            self.codes.append("1")
            self._huffmanCodes(r)
            self.codes.pop()
        else:            
            self.hufftable[tl.value] = ''.join(self.codes)          

    def encode(self, data):    

        self.tf = dict(Counter(data))

        lk  = self.tf.keys()      

        tl = [NodeT(self.tf.get(k),None, None, True, k) for k in lk]
        tl.sort(key=lambda x: x.freq)

        while len(tl)> 1:
            l = tl.pop(0)
            r = tl.pop(0)
            tl.append(NodeT(l.freq + r.freq, l, r, False, None))
            tl.sort(key=lambda x: x.freq)

        self._huffmanCodes(tl.pop(0))

        compressedFile = ''.join([self.hufftable[b] for b in data])

        header_code = self.__encode_hufftable()

        compressedFile = header_code + compressedFile

        cremained = 0
        while not len(compressedFile) % 8 == 0:
            compressedFile += '0'
            cremained += 1

        compressedFile = format(cremained, "08b") + compressedFile
        
        
        return compressedFile


    def __encode_hufftable(self):

        e_table = ''

        #max length symbol
        lms = max(self.hufftable.keys())
        blms = len(bin(lms)) - 2

        #min length codes
        lengths = list(set([len(v) for v in self.hufftable.values()]))
        lengths.sort(reverse = False)
        lmc = min(lengths)
        blmc = len(bin(lmc)) - 2

        #max length of lengths differences
        diffs = self.__get_diffs_lengths(lengths)
        lmd = max(diffs)
        blmd = len(bin(lmd)) - 2
        
        data_huffcodes = self.__data_inv_huffcodes()

        dhc = sorted(data_huffcodes, key=lambda t: t[2])

        sym = format(dhc[0][0], "0" + str(blms) + "b")
        lc = format(lmc, "0" + str(blmc) + "b")
        c = dhc[0][1]

        e_table += sym + lc + c

        last_len = dhc[0][2]

        for i in range(1, len(dhc)):
            sym = format(dhc[i][0], "0" + str(blms) + "b")
            if dhc[i][2] > last_len:
                lc = format(dhc[i][2] - last_len, "0" + str(blmd) + "b")
                last_len = dhc[i][2]
            else:
                lc = format(0, "0" + str(blmd) + "b")
            c =  dhc[i][1]
            e_table += sym + lc + c
        
        header = format(blms, "08b")
        header += format(blmc, "08b")
        header += format(blmd, "08b")
        header += format(len(dhc), "08b")

        return header + e_table        


    def decode(self, datac):


        ht, datac = self.__decode_hufftable(datac)
        lengths = self.__sorted_lengths_by_frequency(ht)

        datad = []
        c_size = len(datac)

        index = 0
        while index < c_size:            
            for l in lengths:
                possible_code = datac[index: index + l]
                if possible_code in ht.keys():
                    datad.append(ht[possible_code])
                    index = index + l
                    break
  
        return datad


    def __decode_hufftable(self, datac):
           
        hufftable = {}
        data_header = []
        header = datac[0:40]
        datac  = datac[40:]
        

        for i in range(0, 40, 8):
            data_header.append(int(header[i:i+8], 2))

        
        rem = data_header[0]
        lms = data_header[1]
        lmc = data_header[2]
        lmd = data_header[3]
        nc  = data_header[4]

        i = 0
        last_length = 0

        k = int(datac[0:lms], 2)
        datac = datac[lms:]
        length = int(datac[0:lmc], 2)
        datac = datac[lmc:]
        last_length += length
        v = datac[0:last_length]
        datac = datac[last_length:]            
        hufftable[v] =  k 


        while i < nc - 1:
            k = int(datac[0:lms], 2)
            datac = datac[lms:]
            length = int(datac[0:lmd], 2)
            datac = datac[lmd:]
            last_length += length
            v = datac[0:last_length]
            datac = datac[last_length:]       
            hufftable[v] =  k
            i += 1
        
        #removing remainer bits
        if rem > 0:
            datac = datac[:-rem]
        
        return hufftable, datac
    
    
    def __data_inv_huffcodes(self):
        return [(k, v, len(v)) for k, v in self.hufftable.items()]
    
    
    def __get_diffs_lengths(self, lengths): 
        return [ lengths[i+1] - lengths[i] for i in range(len(lengths) - 1)]

    
    def __sorted_lengths_by_frequency(self, ht):

        lengths = list(set([len(k) for k in ht.keys()]))
        lengths.sort(reverse = False)
        return lengths