import multiprocessing as mp
import timeit as tiempo

class Parallel:

    def __init__(self, isencode):
        self.isencode = isencode
        self.cpus = mp.cpu_count()
    
    def execute(self, s, i):

        if self.isencode:
            for i in range(0, len(self.obj)):
                s = self.obj[i].encode(s)
        else:
            for i in range(len(self.obj)-1,-1, -1):
                s = self.obj[i].decode(s)                       
        return s 
        
    def parallel(self, seq, chunk_size, obj):
        self.chunk_size  = chunk_size
        self.obj  = obj

        pool = mp.Pool(processes=self.cpus)
        
        results = [pool.apply_async(self.execute, args=(seq[x:x+self.chunk_size], x)) for x in range(0, len(seq), self.chunk_size)]
        outputs = [p.get() for p in results]

        output = []
        if isinstance(outputs[0], str) and not self.isencode:
            output = ''.join(out for out in outputs)
        else:
            for _list in outputs:
                output += _list

        return output