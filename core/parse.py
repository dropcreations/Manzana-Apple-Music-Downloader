import os
import m3u8
import aiohttp
import asyncio
import unicodedata

def sanitize(f):
    b = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\0']
    f = ''.join(c for c in f if c not in b)
    f = ''.join(c for c in f if 31 < ord(c))
    f = unicodedata.normalize("NFKD", f)
    f = f.rstrip(". ")
    return f.strip()

def opt(d: dict):
    nd = {}
    for k, v in d.items():
        if v: nd[k] = v
    return nd

def input_urls(urls: list):
    ret = []

    for url in urls:
        if os.path.exists(url):
            if os.path.splitext(url)[1] == '.txt':
                with open(url, 'r+') as fp:
                    ut = fp.read().split('\n')
                    for u in ut:
                        if u: ret.append(u.strip())
        else: ret.append(url)
    
    return ret

def get_size(urls: list):
    async def contentLength(url):
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                return response.content_length

    loop = asyncio.get_event_loop()
    tasks = [contentLength(url) for url in urls]
    totalContentLength = loop.run_until_complete(asyncio.gather(*tasks))
    
    return sum(totalContentLength)

def aud_uri(uri):
    data = m3u8.load(uri)
    return {
        "type": "audio",
        "uri": data.base_uri + data.segment_map[0].uri,
        "pssh": data.keys[0].uri.split(',')[1]
    }

def mv_uri(url):
    streams = []
    data = m3u8.load(url)

    accessibleAudios = [audio for audio in data.media if audio.type == "AUDIO"]
    accessibleVideos = data.playlists

    for __audio in accessibleAudios:
        streams.append(
            {
                "type": "audio",
                "codec": "HE-AAC" if "HE" in __audio.group_id else "AAC",
                "bitrate": __audio.group_id.split('-')[-1] + " kb/s",
                "language": __audio.language,
                "name": __audio.name,
                "channels": __audio.channels,
                "uri": __audio.uri
            }
        )

    for __video in accessibleVideos:
        streams.append(
            {
                "type": "video",
                "codec": "AVC" if "avc" in __video.stream_info.codecs else "HEVC",
                "bitrate": f'{round((__video.stream_info.average_bandwidth)/1000000, 2)} Mb/s',
                "resolution": f'{__video.stream_info.resolution[0]}x{__video.stream_info.resolution[1]}',
                "fps": __video.stream_info.frame_rate,
                "range": __video.stream_info.video_range,
                "uri": __video.uri
            }
        )

    return streams

def mv_psshs(streams: list):
    async def parse(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                data = data.strip()

                uris = []
                isKey = False
                keyUri = ""

                for line in data.split('\n'):
                    if line.startswith('#EXT-X-KEY'):
                        if "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed" in line:
                            isKey = True
                            for split in line.split('"'):
                                if split.startswith('data:text/plain'):
                                    keyUri = split

                    if '#EXT-X-DISCONTINUITY' in line:
                        isKey = False
                    else:
                        if isKey:
                            if line.startswith('#EXT-X-MAP:URI'):
                                uris.append(os.path.dirname(url) + '/' + line.replace('#EXT-X-MAP:URI="', '').replace('"', ''))
                            if not line.startswith('#'):
                                uris.append(os.path.dirname(url) + '/' + line)

                return [uris, keyUri.split(',')[1]]

    loop = asyncio.get_event_loop()
    tasks = [parse(stream["uri"]) for stream in streams]
    parses = loop.run_until_complete(asyncio.gather(*tasks))

    for i, stream in enumerate(streams):
        stream["uri"] = parses[i][0]
        stream["pssh"] = parses[i][1]

    return list(set([pssh[1] for pssh in parses]))