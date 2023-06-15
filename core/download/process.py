import subprocess
from binaries import MP4BOX, MP4DECRYPT, FFMPEG, CCEXTRACTOR

def decrypt(input, output, key):
    cmd_args = [MP4DECRYPT,
                "--key", f"1:{key}",
                input, output]
    
    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT).wait()
    except Exception: retCode = 1
    
    return retCode

def cc(input):
    cmd_args = [CCEXTRACTOR, input]

    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except Exception: retCode = 1
    
    return retCode

def muxhls(input, output):
    cmd_args = [MP4BOX, "-add", input, "-new", output]

    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except Exception: retCode = 1
    
    return retCode

def muxmv(video, audio, output, cc=None):
    cmd_args = [FFMPEG,
                '-i', video,
                '-i', audio,
                '-map', '0:v', '-c:v', 'copy',
                '-map', '1:a', '-c:a', 'copy',
                '-movflags', '+faststart', output]
    if cc:
        cmd_args[5:5] = ['-i', cc]
        cmd_args[15:15] = ['-map', '2:s', '-c:s', 'mov_text']
    
    try:
        retCode = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except Exception: retCode = 1
    
    return retCode