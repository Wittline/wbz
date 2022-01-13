
from __future__ import absolute_import
import timeit as tiempo
from filehandler import FileHandler
from bwt import Bwt
from mtf import Mtf
from huffman import Tree
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
        tree = Tree(bw_mtf)        
        tree.codings(tree.root)
        bin_str = tree.seq_to_binstr()
        unicode = tree.binstr_to_unicode(bin_str)
        header = tree.codes_to_header()
        bw_mtf_huff =  header + unicode
        
        return bw_mtf_huff

    def decode(self, seq):

        bwt = Bwt('_', '$')
        mtf = Mtf()
        
        header = seq[:seq.index('\n')]
        print(header)
        unicode = seq[seq.index('\n')+1:]
        codes = Tree.header_to_codes(header)
        binary = Tree.unicode_to_binstr(unicode)
        padding = int(codes['pad'])
        binary = Tree.remove_padding(binary, padding)
        decompressed = Tree.binstr_to_seq(binary, codes)

        prl = Parallel(self.chunk_size + 1, [bwt, mtf], False)
        original = prl.parallel(decompressed)

        return original

if __name__ == '__main__':

    pathfile = 'data/84-0.txt'

    fh = FileHandler(pathfile)
    bzip = bzip2(200)


    inicio = tiempo.default_timer()
    seq = fh.read()
    bw_mtf_huff = bzip.encode(seq)
    fh.write_bytes(bw_mtf_huff)
 
    fin = tiempo.default_timer()
    print("Compression time: " + format(fin-inicio, '.8f'))
    print("--------------------------------------------------------------")


    inicio = tiempo.default_timer()
    seq = fh.read_bytes()    
    original = bzip.decode(seq)
    print(original)
    fin = tiempo.default_timer()
    print("deCompression time: " + format(fin-inicio, '.8f'))






