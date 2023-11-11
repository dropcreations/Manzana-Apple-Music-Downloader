import shutil
import subprocess
from utils import logger

MP4DECRYPT = 'mp4decrypt'
MP4BOX = 'MP4Box'
CCEXTRACTOR = 'ccextractor'

if not shutil.which(MP4DECRYPT):
    logger.error("Unable to find 'mp4decrypt' in PATH!", 1)

if not shutil.which(MP4BOX):
    logger.error("Unable to find 'MP4Box' in PATH!", 1)

if not shutil.which(CCEXTRACTOR):
    logger.error("Unable to find 'ccextractor' in PATH!", 1)

def decrypt(input, output, key):
    cmd_args = [MP4DECRYPT, "--key", f"1:{key}", input, output]

    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except:
        retCode = 1

    return retCode

def cc(input, output):
    cmd_args = [CCEXTRACTOR, input, '-o', output]

    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except:
        retCode = 1
    
    return retCode

def muxhls(input, output):
    cmd_args = [MP4BOX, "-itags", "tool=", "-add", input, "-new", output]

    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except:
        retCode = 1
    
    return retCode

def muxmv(video, audio, output, at, cc=None):
    cmd_args = [MP4BOX,
                '-itags', 'tool=',
                '-add', f'{video}#video:name=:lang=und',
                '-add', f'{audio}#audio:name=:lang={at["language"]}:group=1',
                '-new', output]
    if cc:
        cmd_args[7:7] = ['-add', f'{cc}:group=2']
    
    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except:
        retCode = 1
    
    return retCode
