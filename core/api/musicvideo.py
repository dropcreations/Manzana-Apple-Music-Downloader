from core import parse

def parse_data(data):
    media = {}
    media_list = []

    attr = data["attributes"]

    media["coverUrl"] = attr["artwork"]["url"].format(
        w=attr["artwork"].get("width"),
        h=attr["artwork"].get("height")
    )

    filename = parse.sanitize(
        "{} - {} [{}]{}".format(
            attr.get("artistName"),
            attr.get("name"),
            data.get("id"),
            " [E]" if attr.get("contentRating") == "explicit" else ""
        )
    )

    s = {
        "id": data.get("id"),
        "type": 6,
        "genre": attr.get("genreNames"),
        "releasedate": attr.get("releaseDate"),
        "isrc": attr.get("isrc"),
        "song": attr.get("name"),
        "songartist": attr.get("artistName"),
        "rating": 4 if attr.get("contentRating") == "explicit" else 0,
        "file": filename,
        "dir": "no_dir",
    }

    media_list.append(
        parse.opt(s)
    )
    
    media["tracks"] = media_list
    return media