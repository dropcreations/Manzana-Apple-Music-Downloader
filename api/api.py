import re
import m3u8
import json
import base64
import requests

from base64 import b64encode
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from utils import Keys
from utils import Cache
from utils import Logger
from config import Configure
from widevine import WvDecrypt
from widevine import deviceconfig
try:
    from widevine import WidevinePsshData
except ImportError:
    pass

from api.song import song
from api.album import album
from api.musicvideo import musicVideo

logger = Logger()

HEADERS = {
    'content-type': 'application/json;charset=utf-8',
    'connection': 'keep-alive',
    'accept': 'application/json',
    'origin': 'https://music.apple.com',
    'referer': 'https://music.apple.com/',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

class AppleMusic(object):
    def __init__(self, cache: str, config: str, sync: int, animartwork: bool):
        self.__session = requests.Session()
        self.__session.headers = HEADERS

        self.__keys = Keys(cache)
        self.__cache = Cache(cache)
        self.__config = Configure(config)

        self.sync = sync
        self.animartwork = animartwork

        self.__accessToken()
        self.__mediaUserToken()

    def __checkUrl(self, url):
        try:
            urlopen(url)
            return True
        except (URLError, HTTPError):
            return False

    def __getUrl(self, url):
        __url = urlparse(url)

        if not __url.scheme:
            url = f"https://{url}"

        if __url.netloc == "music.apple.com":
            if self.__checkUrl(url):
                splits = url.split('/')

                id = splits[-1]
                kind = splits[4]

                if kind == "album":
                    if len(id.split('?i=')) > 1:
                        id = id.split('?i=')[1]
                        kind = "song"

                self.kind = kind
                self.id = id

            else: logger.error("URL is invalid!", 1)
        else: logger.error("URL is invalid!", 1)

    def __accessToken(self):
        accessToken = self.__cache.get("accessToken")

        if not accessToken:
            logger.info("Fetching access token from web...")

            response = requests.get('https://music.apple.com/us/browse')
            if response.status_code != 200:
                logger.error("Failed to get music.apple.com! Please re-try...", 1)

            indexJs = re.search('(?<=index)(.*?)(?=\.js")', response.text).group(1)
            response = requests.get(f'https://music.apple.com/assets/index{indexJs}.js')
            if response.status_code != 200:
                logger.error("Failed to get js library! Please re-try...", 1)

            accessToken = re.search('(?=eyJh)(.*?)(?=")', response.text).group(1)
            self.__cache.set("accessToken", accessToken)
        else:
            logger.info("Checking access token found in cache...")

            self.__session.headers.update(
                {
                    'authorization': f'Bearer {accessToken}'
                }
            )

            response = self.__session.get("https://amp-api.music.apple.com/v1/catalog/us/songs/1450330685")

            if response.text == "":
                logger.info("Access token found in cache is expired!")

                self.__cache.delete("access_token")
                self.__accessToken()
        
        self.__session.headers.update(
            {
                'authorization': f'Bearer {accessToken}'
            }
        )

    def __mediaUserToken(self, fromLoop=False):
        if self.__config.get():
            logger.info("Checking media-user-token...")

            self.__session.headers.update(
                {
                    "media-user-token": self.__config.get()
                }
            )

            response = self.__session.get("https://amp-api.music.apple.com/v1/me/storefront")

            if response.status_code == 200:
                response = json.loads(response.text)

                self.storefront = response["data"][0].get("id")
                self.language = response["data"][0]["attributes"].get("defaultLanguageTag")

                self.__session.headers.update(
                    {
                        'accept-language': f'{self.language},en;q=0.9'
                    }
                )
            else:
                logger.error("Invalid media-user-token! Re-enter the token...")
                self.__config.delete()
                self.__config.set()
                self.__mediaUserToken(fromLoop=True)
        else:
            if not fromLoop:
                logger.error("Enter your media-user-token to continue!")
                self.__config.set()
            logger.info("Re-start the program...", 1)

    def __getErrors(self, errors):
        if not isinstance(errors, list):
            errors = [errors]
        for error in errors:
            err_status = error.get("status")
            err_detail = error.get("detail")
            logger.error(f"{err_status} - {err_detail}", 1)

    def __getJson(self):
        logger.info("Fetching api response...")

        cacheKey = f"{self.id}:{self.storefront}"
        __cache = self.__cache.get(cacheKey)
        if __cache:
            logger.info("Using the previous response found in cache...")
            return __cache

        apiUrl = f'https://amp-api.music.apple.com/v1/catalog/{self.storefront}/{self.kind}s/{self.id}'

        if self.kind == "album" or self.kind == "song":
            params = {
                'extend': 'editorialArtwork,editorialVideo',
                'include[songs]': 'albums,lyrics',
                'l': f'{self.language}'
            }

        elif self.kind == "music-video":
            params = {
                'l': f'{self.language}'
            }

        self.__session.params = params

        response = self.__session.get(apiUrl)
        response = json.loads(response.text)

        if not "errors" in response:
            self.__cache.set(cacheKey, response)
            return response
        else: self.__getErrors(response)
    
    def __getWebplayback(self, trackId):
        playbackUrl = "https://play.itunes.apple.com/WebObjects/MZPlay.woa/wa/webPlayback"

        data = {
            'salableAdamId': trackId
        }
        response = self.__session.post(url=playbackUrl, data=json.dumps(data))
        if response.status_code != 200:
            logger.error(f"({response.status_code}) {response.reason}: {response.content}")
            return None
        
        _json = json.loads(response.text)
        if "failureType" in _json: return None

        return _json["songList"][0]
    
    def __getServiceCertificate(self, trackId, keyId, licenseUrl, challenge="CAQ="):
        data = {
            "adamId": trackId,
            "challenge": challenge,
            "isLibrary": False,
            "key-system": "com.widevine.alpha",
            "uri": keyId,
            "user-initiated": True
        }
        response = self.__session.post(url=licenseUrl, data=json.dumps(data))
        if response.status_code != 200:
            logger.error(f"({response.status_code}) {response.reason}: {response.content}")
            return None
        
        _json = json.loads(response.text)
        if not "license" in _json:
            logger.error("Invalid license response!")
            return None
        
        return _json.get("license")
    
    def __widevine(self, trackId, keyId, licenseUrl, cert_data_b64, _type="song"):
        if _type == "song":
            pssh_data = WidevinePsshData()
            pssh_data.algorithm = 1
            pssh_data.key_id.append(base64.b64decode(keyId.split(",")[1]))
            pssh = base64.b64encode(pssh_data.SerializeToString()).decode("utf8")
            wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_data_b64, device=deviceconfig.device_android_generic)
            license_b64 = self.__getServiceCertificate(trackId, keyId, licenseUrl, b64encode(wvdecrypt.get_challenge()).decode("utf-8"))

        elif _type == "mv":
            wvdecrypt = WvDecrypt(init_data_b64=keyId.split(",")[-1], cert_data_b64=cert_data_b64, device=deviceconfig.device_android_generic)
            license_b64 = self.__getServiceCertificate(trackId, keyId, licenseUrl, b64encode(wvdecrypt.get_challenge()).decode("utf-8"))
        
        wvdecrypt.update_license(license_b64)
        correct, keys = wvdecrypt.start_process()
        if correct: return correct, keys

    def __get_asset_info(self, url):
        __m3u8_data = m3u8.load(url)
        __file_name = __m3u8_data.segment_map[0].uri # if doesn't work, reinstall m3u8 module
        __key_id = __m3u8_data.keys[0].uri
        return [__m3u8_data.base_uri + __file_name, __key_id]
    
    def __get_mv_asset_info(self, url):
        __m3u8_data = m3u8.load(url)
        __key_id = next(x for x in __m3u8_data.keys if x.keyformat == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed").uri
        return __key_id

    def __get_mv_assets(self, id, licenseUrl, url):
        __variants = {}

        audios = []
        videos = []
        ccs = []

        _mv_m3u8 = m3u8.load(url)
        _av_audio = [audio for audio in _mv_m3u8.media if audio.type == "AUDIO"]
        _av_cc = [cc for cc in _mv_m3u8.media if cc.type == "CLOSED-CAPTIONS"]
        _av_video = _mv_m3u8.playlists

        for c in _av_cc:
            __ccs = {}

            __ccs["name"] = c.name
            __ccs["language"] = c.language

            ccs.append(__ccs)

        for a in _av_audio:
            __audios = {}

            __audios["codec"] = "HE-AAC" if "HE" in a.group_id else "AAC"
            __audios["bitrate"] = a.group_id.split('-')[-1] + " kb/s"
            __audios["language"] = a.language
            __audios["name"] = a.name
            __audios["channels"] = a.channels
            __audios["uri"] = a.uri

            key_id = self.__get_mv_asset_info(a.uri)
            if not key_id: logger.error("Failed to get audio key id with widevine system id!", 1)
            
            keys = self.__keys.get(key_id.split(',')[1])
            if not keys:
                logger.info("Fetching Service Certificate...")
                cert_data_b64 = self.__getServiceCertificate(id, key_id, licenseUrl)
                if not cert_data_b64: logger.error("Failed to get Service Certificate!", 1)

                logger.info("Requesting License...")
                correct, keys = self.__widevine(id, key_id, licenseUrl, cert_data_b64, _type="mv")
                if not correct or not keys: logger.error("Failed to get license!", 1)

                self.__keys.set(key_id.split(',')[1], keys)

            else: logger.info("Using the key found in cache...")

            __keys = []
            for key in keys:
                kid, key = key.split(":")
                __keys.append((kid, key))

            if len(__keys) > 1: logger.info("Multiple keys found, manual intervention required!", 1)
            else:
                decryptKey = __keys[0][1]
                __audios["decryptKey"] = decryptKey

            audios.append(__audios)

        for v in _av_video:
            __videos = {}
            __videos["resolution"] = f'{v.stream_info.resolution[0]}x{v.stream_info.resolution[1]}'
            __videos["fps"] = v.stream_info.frame_rate
            if "avc" in v.stream_info.codecs: __videos["codec"] = "AVC"
            elif "hvc" in v.stream_info.codecs: __videos["codec"] = "HEVC"
            __videos["range"] = v.stream_info.video_range
            __videos["bitrate"] = f'{round((v.stream_info.average_bandwidth)/1000000, 2)} Mb/s'
            __videos["uri"] = v.uri

            key_id = self.__get_mv_asset_info(v.uri)
            if not key_id: logger.error("Failed to get video key id with widevine system id!", 1)
            
            keys = self.__keys.get(key_id.split(',')[1])
            if not keys:
                logger.info("Fetching service certificate...")
                cert_data_b64 = self.__getServiceCertificate(id, key_id, licenseUrl)
                if not cert_data_b64: logger.error("Failed to get Service Certificate!", 1)

                logger.info("Requesting License...")
                correct, keys = self.__widevine(id, key_id, licenseUrl, cert_data_b64, _type="mv")
                if not correct or not keys: logger.error("Failed to get License!", 1)

                self.__keys.set(key_id.split(',')[1], keys)

            else: logger.info("Using the key found in cache...")

            __keys = []
            for key in keys:
                kid, key = key.split(":")
                __keys.append((kid, key))

            if len(__keys) > 1: logger.info("Multiple keys found, manual intervention required!", 1)
            else:
                decryptKey = __keys[0][1]
                __videos["decryptKey"] = decryptKey

            videos.append(__videos)

        __variants["videos"] = videos
        __variants["audios"] = audios
        __variants["closed-captions"] = ccs

        return __variants
    
    def getStreamInfo(self, id, mediatype):
        if mediatype == 1: mediatype = "song"
        elif mediatype == 6: mediatype = "mv"
        
        info = {}
        logger.info("Getting playback information...")
        
        data = self.__getWebplayback(id)
        if not data: logger.error("Failed to get playback information!", 1)

        licenseUrl = data["hls-key-server-url"]

        if mediatype == "mv":
            assetUrl = data["hls-playlist-url"]
            return self.__get_mv_assets(id, licenseUrl, assetUrl)

        elif mediatype == "song":
            asset = next((x for x in data["assets"] if x["flavor"] == "28:ctrp256"), None)
            if not asset: logger.error("Failed to find 28:ctrp256 asset!", 1)

            assetUrl = self.__get_asset_info(asset.get("URL"))[0]
            info["streamUrl"] = assetUrl

            logger.info("Extracting key ID...")
            keyId = self.__get_asset_info(asset.get("URL"))[1]
            pssh = keyId.split(',')[1]
            keys = self.__keys.get(pssh)

            if not keys:
                logger.info("Getting Service Certificate...")
                cert_data_b64 = self.__getServiceCertificate(id, keyId, licenseUrl)
                if not cert_data_b64: logger.error("Failed to get Service Certificate!", 1)

                logger.info("Requesting License...")
                correct, keys = self.__widevine(id, keyId, licenseUrl, cert_data_b64)
                if not correct or not keys: logger.error("Failed to get License!", 1)

                self.__keys.set(pssh, keys)

            else: logger.info("Using the key found in cache...")

            __keys = []
            for key in keys:
                kid, key = key.split(":")
                __keys.append((kid, key))

            if len(__keys) > 1: logger.info("Multiple keys found, manual intervention required!", 1)
            else:
                decryptKey = __keys[0][1]
                info["decryptKey"] = decryptKey

            metadata = asset.get("metadata")
            if "discCount" in metadata: info["disccount"] = metadata.get("discCount")

            return info

    def getInfo(self, url):
        self.__getUrl(url)

        if self.kind == "album":
            return album(
                self.__getJson(),
                syncpoints=self.sync,
                animartwork=self.animartwork
            )
        elif self.kind == "song":
            return song(
                self.__getJson(),
                syncpoints=self.sync,
                animartwork=self.animartwork
            )
        elif self.kind == "music-video":
            return musicVideo(self.__getJson())