import m3u8
import json

from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import Logger

console = Console()
logger = Logger()

def __getUrls(uri):
    __data = m3u8.load(uri)
    __baseUri = __data.base_uri
    __data = json.loads(
        json.dumps(__data.data)
    )

    initSegment = __data["segment_map"][0]["uri"]
    urls = [__baseUri + initSegment]

    for s in __data["segments"]:
        if "key" in s:
            if s["init_section"]["uri"] == initSegment:
                urls.append(__baseUri + s.get("uri"))

    return urls

def getVideos(data):
    if "videos" in data:
        logger.info("Getting video streams list...")

        ids = []
        streamList = data.get("videos")

        table = Table(box=box.ROUNDED)

        table.add_column("ID", justify="center")
        table.add_column("Codec", justify="left")
        table.add_column("Bitrate", justify="left")
        table.add_column("Resolution", justify="left")
        table.add_column("FPS", justify="center")
        table.add_column("Range", justify="center")

        for i, stream in enumerate(streamList):
            ids.append(i)
            table.add_row(
                str(i),
                stream.get("codec"),
                stream.get("bitrate"),
                stream.get("resolution"),
                str(stream.get("fps")),
                stream.get("range")
            )
        
        print()
        columns = Columns(["       ", table])
        console.print(columns)
        id = int(input("\n\t Enter ID: "))
        print()

        if id in ids: return [__getUrls(streamList[id].get("uri")), streamList[id].get("decryptKey")]
        else: logger.error("ID not found in the list!", 1)
    else: logger.error("No video streams available!", 1)