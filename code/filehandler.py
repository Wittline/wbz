import os
import time

class FileHandler:

    def __init__(self):
        pass

    def read(self, fname, ise):
        
        seq = None
        if os.path.exists(fname):
            name, ext = os.path.splitext(fname)
            if ise:
                if ext in ['.csv']:
                    with open(fname, 'r') as file:
                        seq = file.read()
                else:
                    return {'seq': None, 'status': False, 'msg':'Should be .csv format'}           
            else:
                if ext in ['.wbz']:
                    with open(fname, 'r') as file:
                        seq = file.read()
                else:
                    return {'seq': None, 'status': False, 'msg':'Should be .wbz format'}
            
            return {'seq': seq, 'status': True}
        else:
            return {'seq': None, 'status': False, 'msg': 'File not exist'}


    def write_bytes(self, data, fname, ise):

        if os.path.exists(fname):
            name, ext = os.path.splitext(fname)
            if ise:
                fname = name + '.wbz'
            else:
                fname = name + '_' + f'{time.time_ns()}' + '.csv'

            with open(fname, 'wb') as file:
                file.write(data)

            return {'status': True, 'file':fname, 'msg': ''}
        else:
            return {'status': False, 'file':fname, 'msg': 'File not exist'}

