import multiprocessing as mp
import timeit as tiempo

class Parallel:

    def __init__(self, chunk_size, obj, isencode):
        self.chunk_size  = chunk_size
        self.obj  = obj
        self.isencode = isencode
    
    def execute(self, s, i):
        
        if self.isencode:
            for i in range(0, len(self.obj)):
                s = self.obj[i].encode(s)
        else:
            for i in range(len(self.obj)-1,-1, -1):
                s = self.obj[i].decode(s)                            
        return s 
        
    def parallel(self, seq):
        pool = mp.Pool(processes=mp.cpu_count())
        
        results = [pool.apply_async(self.execute, args=(seq[x:x+self.chunk_size], x)) for x in range(0, len(seq), self.chunk_size)]
        outputs = [p.get() for p in results]

        output = []
        for _list in outputs:
            output += _list

        return output