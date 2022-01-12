
from __future__ import absolute_import
import timeit as tiempo
from filehandler import FileHandler
from bwt import Bwt
from mtf import Mtf
from huffman import Huffman
from parallel import Parallel
import math



class bzip2:

    def __init__(self, chunk_size, len_bytes):
        self.chunk_size = chunk_size


    def encode(self, seq):
        bwt = Bwt('_', '$')
        mtf = Mtf()
        prl = Parallel(self.chunk_size, [bwt, mtf], True)
        bw_mtf = prl.parallel(seq)

        return bw_mtf

    def decode(self, seq):
        bwt = Bwt('_', '$')
        mtf = Mtf()
        prl = Parallel(self.chunk_size + 1, [bwt, mtf], False)
        original = prl.parallel(seq)

        return original

if __name__ == '__main__':

    pathfile = '84-0.txt'

    inicio = tiempo.default_timer()

    fh = FileHandler(pathfile)
    seq = fh.read()
    bz = bzip2(1000, len(seq))
    bw_mtf = bz.encode(seq) 
    fin = tiempo.default_timer()
    print("Compression time: " + format(fin-inicio, '.8f'))



    inicio = tiempo.default_timer()
    original = bz.decode(bw_mtf)
    fin = tiempo.default_timer()
    print("deCompression time: " + format(fin-inicio, '.8f'))






