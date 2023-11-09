from bs4 import BeautifulSoup

def __get_ts(ts):
    ts = str(ts).replace('s', '')
    secs = float(ts.split(':')[-1])

    if ":" in ts:
        mins = ts.split(':')[-2]
    else:
        mins = int(str(secs / 60)[:1])
        secs = float(str(secs % 60))

    return f'{mins:0>2}:{secs:05.2f}'

def parse(ttml):
    ttml = BeautifulSoup(ttml, "lxml")

    lyrics = []
    songwriters = []
    timeSyncedLyrics = []

    songwriter = ttml.find_all("songwriter")

    if len(songwriter) > 0:
        for sw in songwriter:
            songwriters.append(sw.text)

    for line in ttml.find_all("p"):
        lyrics.append(line.text)
        
        if "span" in str(line):
            span = BeautifulSoup(str(line), "lxml")

            for s in span.find_all("span", attrs={'begin': True, 'end': True}):
                begin = __get_ts(s.get("begin"))
                timeSyncedLyrics.append(f"[{begin}]{s.text}")
        else:
            begin = __get_ts(line.get("begin"))
            timeSyncedLyrics.append(f"[{begin}]{line.text}")

    return {
        "lyrics": lyrics,
        "songwriter": songwriters if len(songwriters) > 0 else None,
        "timeSyncedLyrics": timeSyncedLyrics
    }