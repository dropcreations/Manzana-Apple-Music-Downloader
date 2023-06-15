import os
import pickle

class Keys(object):
    def __init__(self, keys: str):
        if not os.path.exists(keys):
            os.makedirs(keys)

        self.__keys = os.path.join(keys, "keys.bin")

        if not os.path.exists(self.__keys):
            __keys = {
                "content-type": "keys"
            }

            with open(self.__keys, 'wb') as k:
                pickle.dump(__keys, k)

    def get(self, key):
        with open(self.__keys, 'rb') as k:
            __keys = pickle.load(k)

        return __keys.get(key)

    def set(self, key, value):
        with open(self.__keys, 'rb') as k:
            __keys = pickle.load(k)

        __keys[key] = value

        with open(self.__keys, 'wb') as k:
            pickle.dump(__keys, k)

    def delete(self, key):
        with open(self.__keys, 'rb') as k:
            __keys = pickle.load(k)

        if key in __keys:
            del __keys[key]

        with open(self.__keys, 'wb') as k:
            pickle.dump(__keys, k)