import argparse

from rich.console import Console
from rich.traceback import install

from core import run
from utils import config

install()

__version__ = '2.3.1'

LOGO = r"""


        [bright_white bold]$$$$$$\$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$\  $$$$$$$\   $$$$$$\  
        $$  _$$  _$$\  \____$$\ $$  __$$\ \____$$  |\____$$\ $$  __$$\  \____$$\ 
        $$ / $$ / $$ | $$$$$$$ |$$ |  $$ |  $$$$ _/ $$$$$$$ |$$ |  $$ | $$$$$$$ |
        $$ | $$ | $$ |$$  __$$ |$$ |  $$ | $$  _/  $$  __$$ |$$ |  $$ |$$  __$$ |
        $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |$$$$$$$$\\$$$$$$$ |$$ |  $$ |\$$$$$$$ |
        \__| \__| \__| \_______|\__|  \__|\________|\_______|\__|  \__| \_______|

                            ──── Apple Music Downloader ────[/]

                            
"""

cons = Console()

def main():
    parser = argparse.ArgumentParser(
        description="Manzana: Apple Music Downloader"
    )
    parser.add_argument(
        '-v',
        '--version',
        version=f"Manzana: Apple Music Downloader v{__version__}",
        action="version"
    )
    parser.add_argument(
        '-a',
        '--anim-cover',
        dest='anim',
        help="save animated artwork. [default: False]",
        action="store_true"
    )
    parser.add_argument(
        '-s',
        '--skip-video',
        dest='skip',
        help="skip music-videos inside albums. [default: False]",
        action="store_true"
    )
    parser.add_argument(
        '-ln',
        '--no-lrc',
        dest='noLrc',
        help="don't save time-synced lyrics. [default: False]",
        action="store_true"
    )
    parser.add_argument(
        '-tn',
        '--no-tags',
        dest='noTags',
        help="don't add credits info. [default: False]",
        action="store_true"
    )
    parser.add_argument(
        '-cn',
        '--no-cover',
        dest='noCover',
        help="don't save album artwork. [default: False]",
        action="store_true"
    )
    parser.add_argument(
        'url',
        nargs='+',
        help="Apple Music URL(s) for artist, album, song or music-video",
        type=str
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    cons.print(LOGO)
    args = main()
    config.get_config()
    run(args)
