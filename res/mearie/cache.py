import os
import os.path
import hashlib
import cPickle as pickle

CACHEDIR = None
PICKLE_PROTOCOL = 2 # for binary protocol

def hash_key(key, cachedir=None):
    if cachedir is None:
        cachedir = CACHEDIR
    if not isinstance(key, str):
        key = pickle.dumps(key, PICKLE_PROTOCOL)
    key = hashlib.sha1(key).hexdigest()
    dir = os.path.join(cachedir, key[:1])
    return dir, key

def get_cache(key, cachedir=None):
    dir, key = hash_key(key, cachedir)
    try:
        data = open(os.path.join(dir, key), 'rb').read()
        return pickle.loads(data)
    except:
        return None

def set_cache(key, data, cachedir=None):
    dir, key = hash_key(key, cachedir)
    data = pickle.dumps(data, PICKLE_PROTOCOL)
    try:
        os.makedirs(dir)
    except:
        pass
    try:
        open(os.path.join(dir, key), 'wb').write(data)
    except:
        pass

