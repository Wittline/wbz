
from __future__ import absolute_import
import timeit as tiempo
from code.filehandler import FileHandler
from code.bwt import Bwt
from code.mtf import Mtf
from code.huffman import Huffman


class Compress:

    def __init__(self, seq):
        self.seq = seq

    def encode(self):
        pass
    
    def decode(self):
        pass

if __name__ == '__main__':

    pathfile = ''

    inicio = tiempo.default_timer()


    fin = tiempo.default_timer()
    print("Compression time: " + format(fin-inicio, '.8f'))