
from __future__ import absolute_import
from re import A
import timeit as tiempo
from filehandler import FileHandler
from bwt import BWT
from mtf import MTF
from huffman import Huffman
from parallel import Parallel
from bitsbytes import BitsBytes
import argparse


class bzip2:

    def __init__(self, fname, chunk_size, sc, verbose):
        self.fname = fname
        self.chunk_size = chunk_size
        self.verbose = verbose
        self.bwt = BWT(sc)
        self.mtf = MTF()
        self.tb = BitsBytes()
        self.huf = Huffman()
        self.fh = FileHandler()               

    def encode(self):

        seq = self.fh.read(args.fname)
        
        prl = Parallel(True)

        bwt_mtf = prl.parallel(seq, self.chunk_size, [self.bwt, self.mtf])

        datac = self.huf.encode(bwt_mtf) 

        size = ((len(datac) // 8) // prl.cpus) * 8

        cdata = prl.parallel(datac, size, [self.tb])

        status = self.fh.write_bytes(bytearray(cdata), self.fname)
        
        return status
        
    def decode(self, seq):

        prl = Parallel(False)
        size = (len(seq) // prl.cpus)        
        datac = prl.parallel(seq, size, [self.tb])        
        datad = self.huf.decode(''.join(sb for sb in datac))
        data = prl.parallel(datad, self.chunk_size + 1, [self.mtf, self.bwt])
                
        return bytearray(data)

if __name__ == '__main__':

    inicio = tiempo.default_timer()
    pathfile = 'data/data.csv'
    pathfilecom = 'data/data_compressed.txt'
    pathfileun = 'data/data_uncompressed.txt'
    fh = FileHandler()
    bzip = bzip2(50000, ';')

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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--Action', 
                        type=str, 
                        help = "Type of actions", 
                        metavar = '', 
                        choices=['encode',
                                'decode'])
    
    parser.add_argument('-f','--fname', type=str, help = "Name file", required=True)    
    parser.add_argument('-cs','--chunk_size', type=str, help = "Chunk size", required=True)
    parser.add_argument('-chr','--special_chr', type=str, help = "Special char", required=True)
    parser.add_argument('-v','--verbose', type=int, help = "Verbose", required=False)

    args = parser.parse_args()
    verbose = False

    if args.verbose is not None:
        if args.verbose == 1:
            verbose = True
        elif args.verbose == 0:
            verbose = False
        else:         
            print("The value: {} assigned to -v or --verbose is invalid, Verbose is inactive".format(args.verbose))


    if args.fname is not None and args.fname!= '':
        if args.chunk_size is not None and args.chunk_size != '':
            if args.special_chr is not None and args.special_chr != '':
                if args.Action == 'encode':
                    bzip = bzip2(args.fname, args.chunk_size, args.special_chr, verbose)                    
                    datac = bzip.encode()                 
                elif args.Action == 'decode':
                    fh = FileHandler()
                    bzip = bzip2(args.chunk_size, args.special_chr, verbose)
                    seq = fh.read(args.fname)
                    datac = bzip.encode(seq)
                    fh.write_bytes(datac, args.fname)                   
                else:
                    print("Action {} is invalid".format(args.Action))
            else:
                print("The argument -chr or --special_chr is missing")
        else:
            print("The argument -cs or --chunk_size is missing")
    else:
        print("The argument -f or --fname is missing")
        

