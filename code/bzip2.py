
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

        bwt = Bwt('_', '$')
        mtf = Mtf()
        prl = Parallel(self.chunk_size, [bwt, mtf], True)
        bw_mtf = prl.parallel(seq)

        # huff = Huffman()
        # bw_mtf_huff = huff.encode(bw_mtf)
        
        return bw_mtf

    def decode(self, seq):

        #huff = Huffman()
        bwt = Bwt('_', '$')
        mtf = Mtf()
        
        # decompressed = huff.decode(seq)
        prl = Parallel(self.chunk_size + 1, [bwt, mtf], False)
        original = prl.parallel(seq)

        return original

if __name__ == '__main__':


    inicio = tiempo.default_timer()
    pathfile = 'data/84-0.txt'
    pathfileun = 'data/84-0_compressed.txt'
    fh = FileHandler()
    bzip = bzip2(100)

   
    seq = fh.read(pathfile)
    bw_mtf_huff = bzip.encode(seq)

    #fh.write_bytes(bw_mtf_huff, 'data/84-0_compressed.txt')
    fin = tiempo.default_timer()
    print("Compression time: " + format(fin-inicio, '.8f'))
    
    # print("--------------------------------------------------------------")

    # inicio = tiempo.default_timer()
    # #seq = fh.read_bytes(pathfileun)
    original = bzip.decode(bw_mtf_huff)
    print(original)
    # #fh.write_bytes(bw_mtf_huff, 'data/84-0_uncompressed.txt')
    # fin = tiempo.default_timer()
    # print("deCompression time: " + format(fin-inicio, '.8f'))






