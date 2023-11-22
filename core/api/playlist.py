from core import parse

from . import lyrics
from . import musicvideo

def __parse_song(index, entry, resources):
    song_id = entry["id"]
    song_rels = entry["relationships"]
    song_attr = entry["attributes"]

    album_id = song_rels["albums"]["data"][0]["id"]
    album_attr = resources["albums"][album_id]["attributes"]

    filename = parse.sanitize(
        "{} - {} [{}]{}".format(
            str(index).zfill(2),
            song_attr.get("name"),
            song_id,
            " [E]" if song_attr.get("contentRating") == "explicit" else ""
        )
    )

    artwork = song_attr["artwork"]
    cover = artwork["url"].format(
        w=artwork["width"],
        h=artwork["height"],
        f="jpg"
    )

    s = {
        "id": song_id,
        "genre": song_attr.get("genreNames"),
        "releasedate": song_attr.get("releaseDate"),
        "trackno": song_attr.get("trackNumber"),
        "isrc": song_attr.get("isrc"),
        "composer": song_attr.get("composerName"),
        "discno": song_attr.get("discNumber"),
        "song": song_attr.get("name"),
        "songartist": song_attr.get("artistName"),
        "rating": 4 if song_attr.get("contentRating") == "explicit" else 0,
        "file": filename,
        "coverUrl": cover,

        "copyright": album_attr.get("copyright"),
        "upc": album_attr.get("upc"),
        "recordlabel": album_attr.get("recordLabel"),
        "trackcount": album_attr.get("trackCount"),
        "album": album_attr.get("name"),
        "albumartist": album_attr.get("artistName"),
    }

    if "credits" in song_rels:
        credits = song_rels["credits"].get("data")

        if credits and len(credits) > 0:
            roles = []
            creds = {}

            for credit in credits:
                credit_id = credit["id"]
                credit_type = credit["type"]
                credit_entry = resources[credit_type].get(credit_id)

                if credit_entry:
                    credit_rels = credit_entry.get("relationships")

                    if credit_rels:
                        for ca in credit_rels["credit-artists"]["data"]:
                            ca_id = ca["id"]
                            ca_type = ca["type"]
                            ca_entry = resources[ca_type].get(ca_id)

                            if ca_entry:
                                for role in ca_entry["attributes"]["roleNames"]:
                                    if not role in roles:
                                        roles.append(role)
                                        creds[role] = [ca_entry["attributes"]["name"]]
                                    else:
                                        roleArtist: list = creds[role]
                                        roleArtist.append(ca_entry["attributes"]["name"])
                                        creds[role] = roleArtist

            s["credits"] = creds

    if song_attr.get('hasLyrics') and song_attr['hasLyrics'] and "lyrics" in song_rels:
        lyrics_data = song_rels["lyrics"].get("data")

        if lyrics_data:
            lyrics_rel = lyrics_data[0]
            lyrics_array = resources.get(lyrics_rel["type"])

            if lyrics_array:
                lyrics_entry = lyrics_array[lyrics_rel["id"]]

                if lyrics_entry and lyrics_entry.get("attributes"):
                    s.update(
                        lyrics.parse(
                            lyrics_entry["attributes"]["ttml"]
                        )
                    )

    s["type"] = 1
    return parse.opt(s)

def __parse_music_video(index, entry):
    # Use the existing musicvideo parse function
    # The format in that URL only replaces {w} and {h} so make sure that {f} is replaced with jpg
    entry["attributes"]["artwork"]["url"] = entry["attributes"]["artwork"]["url"].replace(".{f}",".jpg")
    mv = musicvideo.parse_data(entry)

    track = mv["tracks"][0]
    track["coverUrl"] = mv["coverUrl"]
    track["file"] = "{} - {}".format(
        str(index).zfill(2),
        track["file"]
    )

    track["type"] = 6
    return track

def parse_data(data):
    media = {}
    media_list = []

    id        = data["data"][0]["id"]
    resources = data["resources"]
    playlist  = resources["library-playlists"][id]
    attr      = playlist["attributes"]
    relations = playlist["relationships"]["tracks"]["data"]

    media["dir"] = parse.sanitize(
        "{} [{}]".format(
            attr["name"],
            id
        )
    )

    for index, relation in enumerate(relations):
        lib_entry = resources[relation["type"]][relation["id"]]
        lib_rel = lib_entry["relationships"]["catalog"]["data"][0]
        item_type = lib_rel["type"]
        item_id = lib_rel["id"]
        item_entry = resources[item_type][item_id]

        if item_type == "music-videos":
            media_list.append(
                __parse_music_video(index+1, item_entry)
            )
        elif item_type == "songs":
            media_list.append(
                __parse_song(index+1, item_entry, resources)
            )

    media["tracks"] = media_list
    return media
