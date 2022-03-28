
from __future__ import absolute_import
import timeit as tiempo
from filehandler import FileHandler
from bwt import BWT
from mtf import MTF
from huffman import Huffman
from parallel import Parallel
from bitsbytes import BitsBytes


class bzip2:

    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def encode(self, seq):

        bwt, mtf, tb, huff = BWT(';'), MTF(), BitsBytes(), Huffman()
        prl = Parallel(True)

        bwt_mtf = prl.parallel(seq, self.chunk_size, [bwt, mtf])

        datac = huff.encode(bwt_mtf) 

        size = ((len(datac) // 8) // prl.cpus) * 8

        cdata = prl.parallel(datac, size, [tb])
        
        return bytearray(cdata)
        
    def decode(self, seq):

        bwt, mtf, tb, huff = BWT(';'), MTF(), BitsBytes(), Huffman()
        prl = Parallel(False)

        size = (len(seq) // prl.cpus)        
        datac = prl.parallel(seq, size, [tb])        
        datad = huff.decode(''.join(sb for sb in datac))
        data = prl.parallel(datad, self.chunk_size + 1, [mtf,bwt])
                
        return bytearray(data)

if __name__ == '__main__':

    inicio = tiempo.default_timer()
    pathfile = 'data/data.csv'
    pathfilecom = 'data/data_compressed.txt'
    pathfileun = 'data/data_uncompressed.txt'
    fh = FileHandler()
    bzip = bzip2(30000)    

    inicio = tiempo.default_timer()

    seq = fh.read(pathfile)
    datac = bzip.encode(seq)
    fh.write_bytes(datac, pathfilecom)

    fin = tiempo.default_timer()
    print("encode time: " + format(fin-inicio, '.8f'))


    inicio = tiempo.default_timer()

    seq = fh.read_bytes(pathfilecom)
    datau = bzip.decode(seq)

    fh.write_bytes(datau, pathfileun)
    fin = tiempo.default_timer()
    print("decode time: " + format(fin-inicio, '.8f'))

