def musicVideo(data):
    info = {}
    info["dir"] = ""

    attr = data["data"][0]["attributes"]
    
    __info = {}
    __info["id"] = data["data"][0]["id"]

    if "genreNames" in attr: __info["genre"] = ', '.join(attr.get("genreNames"))
    if "releaseDate" in attr: __info["releasedate"] = attr.get("releaseDate")
    if "isrc" in attr: __info["isrc"] = attr.get("isrc")
    if "name" in attr: __info["track"] = attr.get("name")
    if "artistName" in attr: __info["trackartist"] = attr.get("artistName")

    __file = "{0} - {1} [{2}]".format(
        attr.get("artistName"),
        attr.get("name"),
        data["data"][0]["id"]
    )

    if "contentRating" in attr:
        __info["rating"] = attr.get("contentRating")
        if attr.get("contentRating") == "explicit":
            __file += " [E]"

    __info["file"] = __file
    __info["type"] = 6

    info["tracks"] = [__info]
    return info