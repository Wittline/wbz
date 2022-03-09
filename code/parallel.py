import multiprocessing as mp

class Parallel:

    def __init__(self, chunk_size, obj, isencode):
        self.chunk_size  = chunk_size
        self.obj  = obj        
        self.isencode = isencode
    
    def execute(self, s, i):
        # print("chunk n0: ", i, "text: ", s)
        if self.isencode:
            return self.obj[1].encode(self.obj[0].encode(s))
        else:
            return self.obj[0].decode(self.obj[1].decode(s))
        
    def parallel(self, seq):
        pool = mp.Pool(processes=mp.cpu_count())
        
        results = [pool.apply_async(self.execute, args=(seq[x:x+self.chunk_size], x)) for x in range(0, len(seq), self.chunk_size)]
        outputs = [p.get() for p in results]

        # if self.isencode:
        return [item for sublist in outputs for item in sublist]
        # else:
        #     return ''.join(output for output in outputs)
