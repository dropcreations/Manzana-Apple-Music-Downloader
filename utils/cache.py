import os
import pickle

class Cache(object):
    def __init__(self, cache: str):
        if not os.path.exists(cache):
            os.makedirs(cache)

        self.__cache = os.path.join(cache, "cache.bin")

        if not os.path.exists(self.__cache):
            __cache = {
                "content-type": "cache"
            }

            with open(self.__cache, 'wb') as c:
                pickle.dump(__cache, c)

    def get(self, key):
        with open(self.__cache, 'rb') as c:
            __cache = pickle.load(c)

        return __cache.get(key)

    def set(self, key, value):
        with open(self.__cache, 'rb') as c:
            __cache = pickle.load(c)

        __cache[key] = value

        with open(self.__cache, 'wb') as c:
            pickle.dump(__cache, c)

    def delete(self, key):
        with open(self.__cache, 'rb') as c:
            __cache = pickle.load(c)

        if key in __cache:
            del __cache[key]

        with open(self.__cache, 'wb') as c:
            pickle.dump(__cache, c)