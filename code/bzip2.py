
from __future__ import absolute_import
import timeit as tiempo
from filehandler import FileHandler
from bwt import Bwt
from mtf import Mtf
from huffman import Huffman
from parallel import Parallel
import math


class bzip2:

    def __init__(self, chunk_size):
        self.chunk_size = chunk_size        


    def encode(self, seq):

        bwt = Bwt(';')
        mtf = Mtf()
        prl = Parallel(self.chunk_size, [bwt, mtf], True)
        bw_mtf = prl.parallel(seq)

        print(bw_mtf)

        huff = Huffman()
        datac = huff.encode(bw_mtf)

        return datac
        
    def decode(self, seq):

        huff = Huffman()
        bwt = Bwt(';')
        mtf = Mtf()
        
        decompressed = huff.decode(seq)
        print(decompressed)
        prl = Parallel(self.chunk_size + 1, [bwt, mtf], False)
        original = prl.parallel(decompressed)

        return ''

if __name__ == '__main__':

    inicio = tiempo.default_timer()
    pathfile = 'data/data.csv'
    pathfilecom = 'data/data_compressed.txt'
    pathfileun = 'data/data_uncompressed.txt'
    fh = FileHandler()
    bzip = bzip2(100)
    
    seq = fh.read_bytes(pathfile)

    datac = bzip.encode(seq)
    fh.write_bytes(datac, pathfilecom)

    # seq = fh.read_bytes(pathfilecom)
    # datau = bzip.decode(seq)

    #fh.write_bytes(datau, pathfileun)


    # seq = fh.read_bytes(pathfileun)
    # bzip.decode(seq)


    # original = bzip.decode(bw_mtf_huff)    

    # # fh.write_bytes(bw_mtf_huff, 'data/84-0_compressed.txt')
    # # fin = tiempo.default_timer()
    # # print("Compression time: " + format(fin-inicio, '.8f'))
    
    # # print("--------------------------------------------------------------")

    # # inicio = tiempo.default_timer()
    # # #seq = fh.read_bytes(pathfileun)
    # # original = bzip.decode(bw_mtf_huff)
    # # print(original)
    # # #fh.write_bytes(bw_mtf_huff, 'data/84-0_uncompressed.txt')
    # # fin = tiempo.default_timer()
    # # print("deCompression time: " + format(fin-inicio, '.8f'))






