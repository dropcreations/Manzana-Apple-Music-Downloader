import os
import pickle

class Configure(object):
    def __init__(self, config: str):
        if not os.path.exists(config):
            os.makedirs(config)
        
        self.__config = os.path.join(config, "config.bin")

        if not os.path.exists(self.__config):
            __mediaUserToken = input("\n\tmedia-user-token: ")
            print()

            __config = {
                "content-type": "configuration",
                "mediaUserToken": __mediaUserToken
            }

            with open(self.__config, 'wb') as c:
                pickle.dump(__config, c)

    def get(self):

        with open(self.__config, 'rb') as c:
            __config = pickle.load(c)

        return __config.get("mediaUserToken")

    def set(self):
        __mediaUserToken = input("\n\tmedia-user-token: ")
        print()

        with open(self.__config, 'rb') as c:
            __config = pickle.load(c)

        __config["mediaUserToken"] = __mediaUserToken

        with open(self.__config, 'wb') as c:
            pickle.dump(__config, c)

    def delete(self):

        with open(self.__config, 'rb') as c:
            __config = pickle.load(c)

        if "mediaUserToken" in __config:
            del __config["mediaUserToken"]

        with open(self.__config, 'wb') as c:
            pickle.dump(__config, c)