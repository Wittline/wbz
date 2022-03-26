
from __future__ import absolute_import
import timeit as tiempo
from filehandler import FileHandler
from bwt import Bwt
from mtf import Mtf
from huffman import Huffman
from parallel import Parallel
from bitsbytes import BitsBytes
import math


class bzip2:

    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def encode(self, seq):

        bwt, mtf, tb, huff = Bwt(';'), Mtf(), BitsBytes(), Huffman()
        prl = Parallel(True)

        bwt_mtf = prl.parallel(seq, self.chunk_size, [bwt, mtf])

        datac = huff.encode(bwt_mtf) 

        size = ((len(datac) // 8) // prl.cpus) * 8

        cdata = prl.parallel(datac, size, [tb])
        
        return bytearray(cdata)
        
    def decode(self, seq):

        bwt, mtf, tb, huff = Bwt(';'), Mtf(), BitsBytes(), Huffman()
        prl = Parallel(False)

        size = (len(seq) // prl.cpus)
        datac = prl.parallel(seq, size, [tb])
        print("tobits  END")
        datad = huff.decode(''.join(sb for sb in datac))
        print("HUFFMAN END")

        data = prl.parallel(datad, self.chunk_size + 1, [mtf, bwt])
        print("MTF BWT END")

        return data

if __name__ == '__main__':

    inicio = tiempo.default_timer()
    pathfile = 'data/data.csv'
    pathfilecom = 'data/data_compressed.txt'
    pathfileun = 'data/data_uncompressed.txt'
    fh = FileHandler()
    bzip = bzip2(2000)
    

    print("ENCODING")
    inicio = tiempo.default_timer()

    seq = fh.read(pathfile)
    datac = bzip.encode(seq)
    fh.write_bytes(datac, pathfilecom)

    fin = tiempo.default_timer()
    print("encode time: " + format(fin-inicio, '.8f'))


    print("DECODING")
    inicio = tiempo.default_timer()

    seq = fh.read_bytes(pathfilecom)
    datau = bzip.decode(seq)

    fh.write(datau, pathfileun)
    fin = tiempo.default_timer()
    print("decode time: " + format(fin-inicio, '.8f'))


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






