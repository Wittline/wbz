import multiprocessing as mp

class Parallel:

    def __init__(self, seq, chunk_size, obj, isencode):
        self.seq  = seq,
        self.chunk_size  = chunk_size,
        self.obj  = obj,
        self.isencode = isencode
    
    def execute(self, s, pos):
        if self.isencode:
            return (pos, self.obj.encode(s))
        else:
            return (pos, self.obj.decode(s))
        
    def parallel(self, ):
        pool = mp.Pool(processes=mp.cpu_count())        
        results = [pool.apply_async(self.execute, args=(self.seq[x:x+self.chunk_size], x)) for x in range(0, len(self.seq), self.chunk_size)]
        output = [p.get() for p in results]
        
        return output