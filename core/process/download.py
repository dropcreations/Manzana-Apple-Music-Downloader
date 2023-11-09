import requests

from rich.progress import BarColumn
from rich.progress import DownloadColumn
from rich.progress import Progress
from rich.progress import TextColumn
from rich.progress import TimeRemainingColumn
from rich.progress import TransferSpeedColumn

from core import parse

def download(url, filename):
    if not isinstance(url, list):
        url = [url]

    progress = Progress(
        TextColumn("        "),
        TextColumn("[bold blue]Downloading"), BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        "eta", TimeRemainingColumn()
    )
    
    print()

    with progress:
        taskId = progress.add_task(description='', filename=filename, start=False)
        progress.update(taskId, total=parse.get_size(url))
        with open(filename, "wb") as fd:
            progress.start_task(taskId)
            for u in url:
                r = requests.get(u, stream=True)
                for data in r.iter_content(chunk_size=32768):
                    if data:
                        fd.write(data)
                        progress.update(taskId, advance=len(data))

    print()