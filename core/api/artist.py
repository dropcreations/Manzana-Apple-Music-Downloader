from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

console = Console()

def __user(contents: list):
    ids = []
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Name", justify="left")
    table.add_column("ContentID", justify="left")

    for i, content in enumerate(contents):
        ids.append(i)
        table.add_row(
            str(i),
            content.get("name"),
            content.get("contentId")
        )
    
    print()
    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")
    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    elif id == "all": return [url.get("url") for url in contents]
    else:
        try: id = [int(i.strip()) for i in id.split(',')]
        except: logger.error("Input is invalid!", 1)
        id = list(set(id))

        returnContent = []

        for i in id:
            if i in ids: returnContent.append(contents[i]["url"])
            else: logger.warning(f'ID: {i} not in the list!')

        return returnContent

def get_urls(a, s, m, name):
    table = Table(
        box=box.ROUNDED
    )

    table.add_column("ID", justify="center")
    table.add_column("Kind", justify="center")
    table.add_column("Count", justify="center")

    table.add_row('0', 'albums', str(len(a)))
    table.add_row('1', 'singles', str(len(s)))
    table.add_row('2', 'music-videos', str(len(m)))
    
    print()
    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")
    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    elif id == "all": id = [0, 1, 2]
    else:
        try: id = [int(id.strip()) for id in id.split(',')]
        except: logger.error("Input is invalid!", 1)
        id = list(set(id))

    contents = []

    for i in id:
        if i in [0, 1, 2]:
            if i == 0:
                logger.info(f"Getting {name}'s full-albums...")
                contents += __user(a)
            elif i == 1:
                logger.info(f"Getting {name}'s singles...")
                contents += __user(s)
            else:
                logger.info(f"Getting {name}'s music-videos...")
                contents += __user(m)
        else:
            logger.warning(f'ID: {i} not in the list!')

    return contents