from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

console = Console()

def get_audio(streams):
    logger.info("Getting audio streams list...")

    ids = []
    streamList = [s for s in streams if s['type'] == 'audio']

    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="center")
    table.add_column("Bitrate", justify="left")
    table.add_column("Channels", justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Language", justify="center")

    for i, stream in enumerate(streamList):
        ids.append(i)
        table.add_row(
            str(i),
            stream.get("codec"),
            stream.get("bitrate"),
            str(stream.get("channels")),
            stream.get("name"),
            stream.get("language")
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