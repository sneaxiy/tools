import os
import sys
import atexit  
 
 
class FileLogger(object):
    def __init__(self, path):
        self.fids = [open(path, 'w'), sys.stdout, sys.stderr] 
 
    def write(self, *args, **kwargs):
        for fid in self.fids:
            fid.write(*args, **kwargs)
        self.flush()
 
    def flush(self):
        for fid in self.fids:
            fid.flush()
 
    def close(self):
        self.fids[0].close() 
 
 
def redirect(log_dir=None, rank=None, world_size=None): 
    if rank is None:
        rank = int(os.getenv('RANK', '0'))

    if world_size is None:
        world_size = int(os.getenv('WORLD_SIZE', '1'))

    if log_dir is None:
        log_dir = 'log_{}'.format(world_size) 

    file_name = 'log_{}_{}.log'.format(rank, world_size)
    os.makedirs(log_dir, exist_ok=True)
    logger = FileLogger(os.path.join(log_dir, file_name))
    sys.stdout = logger
    sys.stderr = logger
    atexit.register(lambda: logger.close())
 
    
redirect()
