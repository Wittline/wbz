import timeit as tiempo
from functools import reduce
from collections import Counter
import multiprocessing as mp

if __name__ == '__main__':

    pathfile = ''

    inicio = tiempo.default_timer()


    fin = tiempo.default_timer()
    print("Compression time: " + format(fin-inicio, '.8f'))