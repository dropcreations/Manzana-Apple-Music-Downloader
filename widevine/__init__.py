from widevine import deviceconfig
from widevine.wvdecrypt import WvDecrypt
try:
    from widevine.formats.widevine_pssh_data_pb2 import WidevinePsshData
except ModuleNotFoundError:
    pass