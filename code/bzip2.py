
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

    def __init__(self, chunk_size, sc):
        self.chunk_size = chunk_size        
        self.bwt = BWT(sc)
        self.mtf = MTF()
        self.tb = BitsBytes()
        self.huf = Huffman()

    def encode(self, seq):
        
        prl = Parallel(True)

        bwt_mtf = prl.parallel(seq, self.chunk_size, [self.bwt, self.mtf])

        datac = self.huf.encode(bwt_mtf) 

        size = ((len(datac) // 8) // prl.cpus) * 8

        cdata = prl.parallel(datac, size, [self.tb])
        
        return bytearray(cdata)
        
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
    
    parser.add_argument('-f','--fname', type=str, help = "Name file")    
    parser.add_argument('-cs','--chunk_size', type=str, help = "Chunk size")
    parser.add_argument('-chr','--special_chr', type=str, help = "Special char")

    args = parser.parse_args()

    if args.fname is not None and args.fname!= '':
        if args.chunk_size is not None and args.chunk_size != '':
            if args.special_chr is not None and args.special_chr != '':
                if args.Action == 'encode':
                    print("")
                elif args.Action == 'decode':
                    print("")
                else:
                    print()
            else:
                print("")
        else:
            print("")
    else:
        print("Action is invalid") 
        

    if args.Action == 'encode':
        if args.fname is not None and args.fname!= '' \
        and args.chunk_size is not None and args.chunk_size != '':

        else:
            print("The argument -c is missing")
    elif args.Action == 'decode':
        list_clusters()
    elif args.Action == 'terminate_cluster':
        if args.cluster_id is not None and args.cluster_id!= '':
            terminate_cluster(args.cluster_id)
        else:
            print("The argument -idc is missing")
    elif args.Action == 'add_steps':
        if args.cluster_id is not None and args.sfile is not None\
        and args.cluster_id != '' and args.sfile != '':
            add_steps(args.sfile, args.cluster_id)
        else:
            print("The argument -idc or -steps is missing")
    elif args.Action == 'execute_steps':
        if args.cluster_id is not None and args.cluster_id!= '':
            execute_steps(args.cluster_id)
        else:
            print("The argument -idc is missing")
    else:
        print("Action is invalid")    

