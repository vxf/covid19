import os, time, stat
import hashlib
import pickle

class request_cache:
    '''
    Decorator cache for requests, cache a function call with pickle

    Args:
        max_age (int): Seconds until cache expires
        cache_dir (str): Directory to place the cached files
    '''
    def __init__(self, max_age=3600, cache_dir='.cache'):
        self.max_age = max_age
        self.cache_dir = cache_dir

    def __call__(self, func):
        def wrapper(*args):
            # make sure the cache directory exists
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)

            # cache file name
            h = hashlib.md5(str(args).encode('utf-8')).hexdigest()
            file_name = '{}/{}'.format(self.cache_dir, h)

            # if the cache is valid return the value
            if os.path.isfile(file_name) and self.file_age_in_seconds(file_name) < self.max_age:
                with open(file_name, 'rb') as f:
                    data = pickle.load(f)
                    return data

            # if cache is invalid run the function, save cache and return the value
            data = func(*args)
            with open(file_name, 'wb') as f:
                pickle.dump(data, f)
            return data

        return wrapper

    @staticmethod
    def file_age_in_seconds(pathname):
        '''
        Calculate elapsed seconds since last file modification
        https://stackoverflow.com/a/6879539
        '''
        return time.time() - os.stat(pathname)[stat.ST_MTIME]
