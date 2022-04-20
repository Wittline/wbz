import timeit as tiempo
from filehandler import FileHandler
from bwt import BWT
from mtf import MTF
from huffman import Huffman
from parallel import Parallel
from bitsbytes import BitsBytes
import argparse
import pandas as pd
import numpy as np


class bzip2:

    def __init__(self, fname, chunk_size, sc):
        self.fname = fname
        self.chunk_size = chunk_size        
        self.bwt = BWT(sc)
        self.mtf = MTF()
        self.tb = BitsBytes()
        self.huf = Huffman()
        self.fh = FileHandler()        


    def encode(self):        

        seqreader = self.fh.read(self.fname, True)        

        if seqreader['status']:

            seq = seqreader['seq']
            o_len = len(seq)

            prl = Parallel(True)

            bwt_mtf = prl.parallel(seq, self.chunk_size, [self.bwt, self.mtf])

            datac = self.huf.encode(bwt_mtf)
                        
            size = ((len(datac) // 8) // prl.cpus) * 8

            cdata = prl.parallel(datac, size, [self.tb])             

            seqwriter = self.fh.write_bytes(bytearray(cdata), self.fname, True)

            if not seqwriter['status']:
                print("Issues Writing file {} due to: {} ".format(seqwriter['file'], seqwriter['msg']))
        else:
            print("Issues reading file due to: {} ".format(seqreader['msg'])) 
        
    def decode(self):

        seqreader = self.fh.read(self.fname, False)

        if seqreader['status']:
            
            seq = seqreader['seq']

            prl = Parallel(False)
            size = (len(seq) // prl.cpus)     
            datac = prl.parallel(seq, size, [self.tb])       
            datad = self.huf.decode(''.join(sb for sb in datac))
            data = prl.parallel(datad, self.chunk_size + 1, [self.mtf, self.bwt])
            seqwriter = self.fh.write_bytes(bytearray(data), self.fname, False)

            if not seqwriter['status']:
                print("Issues Writing file {} due to: {} ".format(seqwriter['file'], seqwriter['msg']))
                
        else:
            print("Issues reading file due to: {} ".format(seqreader['msg'])) 


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--Action', 
                        type=str, 
                        help = "Type of actions", 
                        metavar = '', 
                        choices=['encode',
                                'decode', 'performance'])
    
    parser.add_argument('-f','--fname', type=str, help = "Name file", required=True)    
    parser.add_argument('-cs','--chunk_size', type=str, help = "Chunk size", required=True)
    parser.add_argument('-ch','--special_chr', type=str, help = "Special char", required=True)    

    args = parser.parse_args()    

    if args.fname is not None and args.fname!= '':
        if args.chunk_size is not None and args.chunk_size != '':
            if args.special_chr is not None and args.special_chr != '':
                if args.Action == 'encode':
                    bzip = bzip2(args.fname, int(args.chunk_size), args.special_chr)      
                    bzip.encode()
                elif args.Action == 'decode':
                    bzip = bzip2(args.fname, int(args.chunk_size), args.special_chr)                 
                    bzip.decode()
                else:
                    print("Action {} is invalid".format(args.Action))
            else:
                print("The argument -chr or --special_chr is missing")
        else:
            print("The argument -cs or --chunk_size is missing")
    else:
        print("The argument -f or --fname is missing")
        