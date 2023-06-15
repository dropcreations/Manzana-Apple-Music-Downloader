import os
import argparse

from rich.console import Console
from rich.traceback import install

from handler import arguments

install()
console = Console()

LOGO = r"""


        [bright_white bold]$$$$$$\$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$\  $$$$$$$\   $$$$$$\  
        $$  _$$  _$$\  \____$$\ $$  __$$\ \____$$  |\____$$\ $$  __$$\  \____$$\ 
        $$ / $$ / $$ | $$$$$$$ |$$ |  $$ |  $$$$ _/ $$$$$$$ |$$ |  $$ | $$$$$$$ |
        $$ | $$ | $$ |$$  __$$ |$$ |  $$ | $$  _/  $$  __$$ |$$ |  $$ |$$  __$$ |
        $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |$$$$$$$$\\$$$$$$$ |$$ |  $$ |\$$$$$$$ |
        \__| \__| \__| \_______|\__|  \__|\________|\_______|\__|  \__| \_______|

                            ──── Apple Music Downloader ────[/]


"""

def main():
    parser = argparse.ArgumentParser(
        description="Manzana: Apple Music Downloader"
    )
    parser.add_argument(
        '-s',
        '--sync',
        help="Save timecode's in 00:00.000 format (three ms points)",
        action="store_true"
    )
    parser.add_argument(
        '-a',
        '--anim',
        help="Download the animated artwork if available",
        action="store_true"
    )
    parser.add_argument(
        '--no-cover',
        help="Don't save album artwork",
        action="store_true"
    )
    parser.add_argument(
        '--no-lrc',
        help="Don't save time-synced lyrics as a .lrc file",
        action="store_true"
    )
    parser.add_argument(
        'url',
        help="Apple Music URL for an album, a song or a music-video",
        type=str
    )
    args = parser.parse_args()
    arguments(args)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(LOGO)
    main()