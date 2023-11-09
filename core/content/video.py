from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

console = Console()

def get_video(streams):
    logger.info("Getting video streams list...")

    ids = []
    streamList = [s for s in streams if s['type'] == 'video']

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
    id = input("\n\t Enter ID: ")
    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    else:
        try: id = int(id)
        except: logger.error("Invalid input!", 1)

    if id in ids: return streamList[id]
    else: logger.error("ID not found in the list!", 1)