import os
import signal

from threading import Event
from functools import partial
from urllib.request import urlopen

from utils import Logger

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn
)

doneEvent = Event()
logger = Logger()

def handleSigint(signum, frame):
    doneEvent.set()

signal.signal(signal.SIGINT, handleSigint)

def download(url, dir, file, log):
    logger.info(log)
    if not isinstance(url, list): url = [url]
    destPath = os.path.join(dir, file)

    print()

    progress = Progress(
        TextColumn("        "),
        TextColumn("[bold blue]Downloading"), BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        "eta", TimeRemainingColumn()
    )

    def __getUrl(taskId: TaskID, urls: list, path: str) -> None:
        total = 0
        for url in urls:
            response = urlopen(url)
            total += int(response.info()["Content-length"])
        progress.update(taskId, total=total)

        with open(path, "wb") as d:
            progress.start_task(taskId)

            for url in urls:
                response = urlopen(url)
                for data in iter(partial(response.read, 32768), b""):
                    d.write(data)
                    progress.update(taskId, advance=len(data))

                    if doneEvent.is_set():
                        return
    
    with progress:
        taskId = progress.add_task("download",
                                   filename=file,
                                   start=False)
        __getUrl(taskId, url, destPath)

    print()