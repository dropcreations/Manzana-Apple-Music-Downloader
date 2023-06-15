from bs4 import BeautifulSoup

def __getTs(ts, syncpoints: int):
    ts = str(ts).replace('s', '')
    secs = float(ts.split(':')[-1])

    if ":" in ts:
        mins = ts.split(':')[-2]
    else:
        mins = int(str(secs / 60)[:1])
        secs = float(str(secs % 60))

    if syncpoints == 3: return f'{mins:0>2}:{secs:06.3f}'
    elif syncpoints == 2: return f'{mins:0>2}:{secs:05.2f}'

def getLyrics(ttml, syncpoints: int):
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
                begin = __getTs(s.get("begin"), syncpoints)
                timeSyncedLyrics.append(f"[{begin}]{s.text}")
        else:
            begin = __getTs(line.get("begin"), syncpoints)
            timeSyncedLyrics.append(f"[{begin}]{line.text}")

    return {
        "lyrics": lyrics,
        "songwriter": ', '.join(songwriters) if len(songwriters) > 0 else None,
        "timeSyncedLyrics": timeSyncedLyrics
    }