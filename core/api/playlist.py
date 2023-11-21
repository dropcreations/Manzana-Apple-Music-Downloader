from core import parse

from . import lyrics

"""
Example response:
{
    "data":[
        {
            "id":"p.zp6KlMvsB3XNYNY",
            "type":"library-playlists",
            "href":"/v1/me/library/playlists/p.zp6KlMvsB3XNYNY?l=ro"
        }
    ],
    "resources":{
        "library-playlists":{
            "p.zp6KlMvsB3XNYNY":{
                "id":"p.zp6KlMvsB3XNYNY",
                "type":"library-playlists",
                "href":"/v1/me/library/playlists/p.zp6KlMvsB3XNYNY?l=ro",
                "attributes":{
                    "hasCollaboration":false,
                    "lastModifiedDate":"2023-11-21T17:00:40Z",
                    "canEdit":true,
                    "name":"Test",
                    "description":{
                        "standard":"Test"
                    },
                    "isPublic":false,
                    "canDelete":true,
                    "hasCatalog":false,
                    "playParams":{
                        "id":"p.zp6KlMvsB3XNYNY",
                        "kind":"playlist",
                        "isLibrary":true
                    },
                    "dateAdded":"2023-11-21T16:59:58Z"
                },
                "relationships":{
                    "tracks":{
                        "href":"/v1/me/library/playlists/p.zp6KlMvsB3XNYNY/tracks?l=ro",
                        "data":[
                            {
                                "id":"i.06QNbW2T0koOEOE",
                                "type":"library-songs",
                                "href":"/v1/me/library/songs/i.06QNbW2T0koOEOE?l=ro"
                            },
                            {
                                "id":"i.xrXvNqxHMY1AoAo",
                                "type":"library-songs",
                                "href":"/v1/me/library/songs/i.xrXvNqxHMY1AoAo?l=ro"
                            },
                            {
                                "id":"i.EYVb8WMtmA9eDeD",
                                "type":"library-songs",
                                "href":"/v1/me/library/songs/i.EYVb8WMtmA9eDeD?l=ro"
                            },
                            {
                                "id":"i.xrXvRlvUMY1AoAo",
                                "type":"library-songs",
                                "href":"/v1/me/library/songs/i.xrXvRlvUMY1AoAo?l=ro"
                            }
                        ],
                        "meta":{
                            "total":4
                        }
                    },
                    "catalog":{
                        "href":"/v1/me/library/playlists/p.zp6KlMvsB3XNYNY/catalog?l=ro",
                        "data":[
                            
                        ]
                    }
                }
            }
        },
        "library-songs":{
            "i.EYVb8WMtmA9eDeD":{
                "id":"i.EYVb8WMtmA9eDeD",
                "type":"library-songs",
                "href":"/v1/me/library/songs/i.EYVb8WMtmA9eDeD?l=ro",
                "attributes":{
                    "discNumber":1,
                    "albumName":"Hurt (feat. Danyka Nadeau) - Single",
                    "hasCredits":false,
                    "genreNames":[
                        "Trance"
                    ],
                    "hasLyrics":false,
                    "trackNumber":1,
                    "releaseDate":"2018-01-26",
                    "durationInMillis":211413,
                    "name":"Hurt (feat. Danyka Nadeau)",
                    "artistName":"Jeremy Vancaulart",
                    "artwork":{
                        "width":1200,
                        "height":1200,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music118/v4/73/a9/da/73a9daa1-c9f1-9e5f-f9ca-be5b99a36319/8718522184888.png/{w}x{h}bb.{f}",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"i.EYVb8WMtmA9eDeD",
                        "kind":"song",
                        "isLibrary":true,
                        "reporting":true,
                        "catalogId":"1334280149",
                        "reportingId":"1334280149"
                    }
                },
                "relationships":{
                    "catalog":{
                        "href":"/v1/me/library/songs/i.EYVb8WMtmA9eDeD/catalog?l=ro",
                        "data":[
                            {
                                "id":"1334280149",
                                "type":"songs",
                                "href":"/v1/catalog/ro/songs/1334280149?l=ro"
                            }
                        ]
                    }
                }
            },
            "i.xrXvRlvUMY1AoAo":{
                "id":"i.xrXvRlvUMY1AoAo",
                "type":"library-songs",
                "href":"/v1/me/library/songs/i.xrXvRlvUMY1AoAo?l=ro",
                "attributes":{
                    "discNumber":1,
                    "albumName":"Above & Beyond Presents OceanLab Sirens of the Sea REMIXED",
                    "hasCredits":false,
                    "genreNames":[
                        "Dance"
                    ],
                    "hasLyrics":true,
                    "trackNumber":17,
                    "releaseDate":"2003-01-01",
                    "durationInMillis":447530,
                    "name":"Satellite (Original Above & Beyond Mix)",
                    "artistName":"OceanLab",
                    "artwork":{
                        "width":1200,
                        "height":1200,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/31/65/6b/mzi.navynbso.jpg/{w}x{h}bb.{f}",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"i.xrXvRlvUMY1AoAo",
                        "kind":"song",
                        "isLibrary":true,
                        "reporting":true,
                        "catalogId":"316215865",
                        "reportingId":"316215865"
                    }
                },
                "relationships":{
                    "catalog":{
                        "href":"/v1/me/library/songs/i.xrXvRlvUMY1AoAo/catalog?l=ro",
                        "data":[
                            {
                                "id":"316215865",
                                "type":"songs",
                                "href":"/v1/catalog/ro/songs/316215865?l=ro"
                            }
                        ]
                    }
                }
            },
            "i.06QNbW2T0koOEOE":{
                "id":"i.06QNbW2T0koOEOE",
                "type":"library-songs",
                "href":"/v1/me/library/songs/i.06QNbW2T0koOEOE?l=ro",
                "attributes":{
                    "discNumber":1,
                    "albumName":"A State of Trance - 15 Years",
                    "hasCredits":false,
                    "genreNames":[
                        "Trance"
                    ],
                    "hasLyrics":true,
                    "trackNumber":9,
                    "releaseDate":"2015-06-01",
                    "durationInMillis":270507,
                    "name":"Anahera",
                    "artistName":"Ferry Corsten & Gouryella",
                    "artwork":{
                        "width":1200,
                        "height":1200,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/95/7d/f5/957df58d-e948-8666-3b90-c9362062e25d/8718522112805.png/{w}x{h}bb.{f}",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"i.06QNbW2T0koOEOE",
                        "kind":"song",
                        "isLibrary":true,
                        "reporting":true,
                        "catalogId":"1151491184",
                        "reportingId":"1151491184"
                    }
                },
                "relationships":{
                    "catalog":{
                        "href":"/v1/me/library/songs/i.06QNbW2T0koOEOE/catalog?l=ro",
                        "data":[
                            {
                                "id":"1151491184",
                                "type":"songs",
                                "href":"/v1/catalog/ro/songs/1151491184?l=ro"
                            }
                        ]
                    }
                }
            },
            "i.xrXvNqxHMY1AoAo":{
                "id":"i.xrXvNqxHMY1AoAo",
                "type":"library-songs",
                "href":"/v1/me/library/songs/i.xrXvNqxHMY1AoAo?l=ro",
                "attributes":{
                    "discNumber":1,
                    "albumName":"Lange Presents Intercity 100",
                    "hasCredits":false,
                    "genreNames":[
                        "Dance"
                    ],
                    "hasLyrics":true,
                    "trackNumber":29,
                    "releaseDate":"2010-03-29",
                    "durationInMillis":356734,
                    "name":"Right Back",
                    "artistName":"Yuri Kane",
                    "artwork":{
                        "width":1200,
                        "height":1200,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/v4/70/ff/41/70ff41e6-faf8-de2f-764c-5243891bc8dc/cover.jpg/{w}x{h}bb.{f}",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"i.xrXvNqxHMY1AoAo",
                        "kind":"song",
                        "isLibrary":true,
                        "reporting":true,
                        "catalogId":"556406361",
                        "reportingId":"556406361"
                    }
                },
                "relationships":{
                    "catalog":{
                        "href":"/v1/me/library/songs/i.xrXvNqxHMY1AoAo/catalog?l=ro",
                        "data":[
                            {
                                "id":"556406361",
                                "type":"songs",
                                "href":"/v1/catalog/ro/songs/556406361?l=ro"
                            }
                        ]
                    }
                }
            }
        },
        "songs":{
            "316215865":{
                "id":"316215865",
                "type":"songs",
                "href":"/v1/catalog/ro/songs/316215865?l=ro",
                "attributes":{
                    "hasTimeSyncedLyrics":true,
                    "albumName":"Above & Beyond Presents OceanLab Sirens of the Sea REMIXED",
                    "genreNames":[
                        "Dance",
                        "Muzică",
                        "Muzică electronică"
                    ],
                    "trackNumber":17,
                    "releaseDate":"2003-01-01",
                    "durationInMillis":447530,
                    "isVocalAttenuationAllowed":true,
                    "isMasteredForItunes":false,
                    "isrc":"GBARL0400878",
                    "artwork":{
                        "width":1780,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/31/65/6b/mzi.navynbso.jpg/{w}x{h}bb.{f}",
                        "height":1780,
                        "textColor3":"789ba6",
                        "textColor2":"7cb4ca",
                        "textColor4":"6792a3",
                        "textColor1":"90c0ce",
                        "bgColor":"170908",
                        "hasP3":false
                    },
                    "audioLocale":"en-US",
                    "url":"https://music.apple.com/ro/album/satellite-original-above-beyond-mix/316215796?i=316215865&l=ro",
                    "playParams":{
                        "id":"316215865",
                        "kind":"song"
                    },
                    "discNumber":1,
                    "hasCredits":false,
                    "hasLyrics":true,
                    "isAppleDigitalMaster":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "name":"Satellite (Original Above & Beyond Mix)",
                    "previews":[
                        {
                            "url":"https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/ab/d8/f5/abd8f5e7-858b-2634-b7fa-1f520718cf0d/mzaf_8133965542896677072.plus.aac.ep.m4a"
                        }
                    ],
                    "artistName":"OceanLab"
                },
                "relationships":{
                    "credits":{
                        "href":"/v1/catalog/ro/songs/316215865/credits?l=ro",
                        "data":[
                            {
                                "id":"316215865-4",
                                "type":"role-categories"
                            },
                            {
                                "id":"316215865-3",
                                "type":"role-categories"
                            },
                            {
                                "id":"316215865-5",
                                "type":"role-categories"
                            }
                        ]
                    },
                    "albums":{
                        "href":"/v1/catalog/ro/songs/316215865/albums?l=ro",
                        "data":[
                            {
                                "id":"316215796",
                                "type":"albums",
                                "href":"/v1/catalog/ro/albums/316215796?l=ro"
                            }
                        ]
                    },
                    "artists":{
                        "href":"/v1/catalog/ro/songs/316215865/artists?l=ro",
                        "data":[
                            {
                                "id":"18214657",
                                "type":"artists",
                                "href":"/v1/catalog/ro/artists/18214657?l=ro"
                            }
                        ]
                    },
                    "lyrics":{
                        "href":"/v1/catalog/ro/songs/316215865/lyrics?l=ro",
                        "data":[
                            {
                                "id":"316215865",
                                "type":"lyrics"
                            }
                        ]
                    }
                }
            },
            "1334280149":{
                "id":"1334280149",
                "type":"songs",
                "href":"/v1/catalog/ro/songs/1334280149?l=ro",
                "attributes":{
                    "hasTimeSyncedLyrics":false,
                    "albumName":"Hurt (feat. Danyka Nadeau) - Single",
                    "genreNames":[
                        "Trance",
                        "Muzică",
                        "Dance"
                    ],
                    "trackNumber":1,
                    "releaseDate":"2018-01-26",
                    "durationInMillis":211413,
                    "isVocalAttenuationAllowed":false,
                    "isMasteredForItunes":false,
                    "isrc":"NLF711800214",
                    "artwork":{
                        "width":3000,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music118/v4/73/a9/da/73a9daa1-c9f1-9e5f-f9ca-be5b99a36319/8718522184888.png/{w}x{h}bb.{f}",
                        "height":3000,
                        "textColor3":"272c28",
                        "textColor2":"161616",
                        "textColor4":"2b2e29",
                        "textColor1":"111316",
                        "bgColor":"808e74",
                        "hasP3":false
                    },
                    "audioLocale":"zxx",
                    "composerName":"J. Vancaulart & D. Nadeau",
                    "url":"https://music.apple.com/ro/album/hurt-feat-danyka-nadeau/1334280142?i=1334280149&l=ro",
                    "playParams":{
                        "id":"1334280149",
                        "kind":"song"
                    },
                    "discNumber":1,
                    "hasCredits":false,
                    "hasLyrics":false,
                    "isAppleDigitalMaster":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "name":"Hurt (feat. Danyka Nadeau)",
                    "previews":[
                        {
                            "url":"https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview125/v4/b7/17/23/b717239f-6add-d22a-2761-a8776192540e/mzaf_4295964746136061084.plus.aac.ep.m4a"
                        }
                    ],
                    "artistName":"Jeremy Vancaulart"
                },
                "relationships":{
                    "credits":{
                        "href":"/v1/catalog/ro/songs/1334280149/credits?l=ro",
                        "data":[
                            {
                                "id":"1334280149-4",
                                "type":"role-categories"
                            },
                            {
                                "id":"1334280149-3",
                                "type":"role-categories"
                            },
                            {
                                "id":"1334280149-5",
                                "type":"role-categories"
                            }
                        ]
                    },
                    "albums":{
                        "href":"/v1/catalog/ro/songs/1334280149/albums?l=ro",
                        "data":[
                            {
                                "id":"1334280142",
                                "type":"albums",
                                "href":"/v1/catalog/ro/albums/1334280142?l=ro"
                            }
                        ]
                    },
                    "artists":{
                        "href":"/v1/catalog/ro/songs/1334280149/artists?l=ro",
                        "data":[
                            {
                                "id":"562637194",
                                "type":"artists",
                                "href":"/v1/catalog/ro/artists/562637194?l=ro"
                            }
                        ]
                    },
                    "lyrics":{
                        "href":"/v1/catalog/ro/songs/1334280149/lyrics?l=ro",
                        "data":[
                            
                        ]
                    }
                }
            },
            "1151491184":{
                "id":"1151491184",
                "type":"songs",
                "href":"/v1/catalog/ro/songs/1151491184?l=ro",
                "attributes":{
                    "hasTimeSyncedLyrics":false,
                    "albumName":"A State of Trance - 15 Years",
                    "genreNames":[
                        "Trance",
                        "Muzică",
                        "Dance"
                    ],
                    "trackNumber":9,
                    "releaseDate":"2015-06-01",
                    "durationInMillis":270507,
                    "isVocalAttenuationAllowed":false,
                    "isMasteredForItunes":false,
                    "isrc":"NLQ881500055",
                    "artwork":{
                        "width":3000,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/95/7d/f5/957df58d-e948-8666-3b90-c9362062e25d/8718522112805.png/{w}x{h}bb.{f}",
                        "height":3000,
                        "textColor3":"d3d2d2",
                        "textColor2":"fba117",
                        "textColor4":"d08819",
                        "textColor1":"ffffff",
                        "bgColor":"252120",
                        "hasP3":false
                    },
                    "audioLocale":"en-US",
                    "composerName":"Ferry Corsten",
                    "url":"https://music.apple.com/ro/album/anahera/1151490543?i=1151491184&l=ro",
                    "playParams":{
                        "id":"1151491184",
                        "kind":"song"
                    },
                    "discNumber":1,
                    "hasCredits":false,
                    "hasLyrics":true,
                    "isAppleDigitalMaster":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "name":"Anahera",
                    "previews":[
                        {
                            "url":"https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview125/v4/fc/fb/b7/fcfbb737-a637-2aec-f976-7fd49d84a9a6/mzaf_4641990365154209584.plus.aac.ep.m4a"
                        }
                    ],
                    "artistName":"Ferry Corsten & Gouryella"
                },
                "relationships":{
                    "credits":{
                        "href":"/v1/catalog/ro/songs/1151491184/credits?l=ro",
                        "data":[
                            {
                                "id":"1151491184-4",
                                "type":"role-categories"
                            },
                            {
                                "id":"1151491184-3",
                                "type":"role-categories"
                            },
                            {
                                "id":"1151491184-5",
                                "type":"role-categories"
                            }
                        ]
                    },
                    "albums":{
                        "href":"/v1/catalog/ro/songs/1151491184/albums?l=ro",
                        "data":[
                            {
                                "id":"1151490543",
                                "type":"albums",
                                "href":"/v1/catalog/ro/albums/1151490543?l=ro"
                            }
                        ]
                    },
                    "artists":{
                        "href":"/v1/catalog/ro/songs/1151491184/artists?l=ro",
                        "data":[
                            {
                                "id":"3688902",
                                "type":"artists",
                                "href":"/v1/catalog/ro/artists/3688902?l=ro"
                            },
                            {
                                "id":"44166471",
                                "type":"artists",
                                "href":"/v1/catalog/ro/artists/44166471?l=ro"
                            }
                        ]
                    },
                    "lyrics":{
                        "href":"/v1/catalog/ro/songs/1151491184/lyrics?l=ro",
                        "data":[
                            {
                                "id":"1151491184",
                                "type":"lyrics"
                            }
                        ]
                    }
                }
            },
            "556406361":{
                "id":"556406361",
                "type":"songs",
                "href":"/v1/catalog/ro/songs/556406361?l=ro",
                "attributes":{
                    "hasTimeSyncedLyrics":true,
                    "albumName":"Lange Presents Intercity 100",
                    "genreNames":[
                        "Dance",
                        "Muzică"
                    ],
                    "trackNumber":29,
                    "releaseDate":"2010-03-29",
                    "durationInMillis":356734,
                    "isVocalAttenuationAllowed":true,
                    "isMasteredForItunes":false,
                    "isrc":"GBKQU1210326",
                    "artwork":{
                        "width":2400,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/v4/70/ff/41/70ff41e6-faf8-de2f-764c-5243891bc8dc/cover.jpg/{w}x{h}bb.{f}",
                        "height":2400,
                        "textColor3":"c28363",
                        "textColor2":"daa170",
                        "textColor4":"b4865d",
                        "textColor1":"eb9d78",
                        "bgColor":"1d1a11",
                        "hasP3":false
                    },
                    "audioLocale":"en-US",
                    "url":"https://music.apple.com/ro/album/right-back/556406001?i=556406361&l=ro",
                    "playParams":{
                        "id":"556406361",
                        "kind":"song"
                    },
                    "discNumber":1,
                    "hasCredits":false,
                    "hasLyrics":true,
                    "isAppleDigitalMaster":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "name":"Right Back",
                    "previews":[
                        {
                            "url":"https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/72/f4/c3/72f4c3d3-ca52-2cd7-4f99-12da23bc0a4f/mzaf_834022184971366575.plus.aac.ep.m4a"
                        }
                    ],
                    "artistName":"Yuri Kane"
                },
                "relationships":{
                    "credits":{
                        "href":"/v1/catalog/ro/songs/556406361/credits?l=ro",
                        "data":[
                            {
                                "id":"556406361-4",
                                "type":"role-categories"
                            },
                            {
                                "id":"556406361-3",
                                "type":"role-categories"
                            },
                            {
                                "id":"556406361-5",
                                "type":"role-categories"
                            }
                        ]
                    },
                    "albums":{
                        "href":"/v1/catalog/ro/songs/556406361/albums?l=ro",
                        "data":[
                            {
                                "id":"556406001",
                                "type":"albums",
                                "href":"/v1/catalog/ro/albums/556406001?l=ro"
                            }
                        ]
                    },
                    "artists":{
                        "href":"/v1/catalog/ro/songs/556406361/artists?l=ro",
                        "data":[
                            {
                                "id":"342853516",
                                "type":"artists",
                                "href":"/v1/catalog/ro/artists/342853516?l=ro"
                            }
                        ]
                    },
                    "lyrics":{
                        "href":"/v1/catalog/ro/songs/556406361/lyrics?l=ro",
                        "data":[
                            {
                                "id":"556406361",
                                "type":"lyrics"
                            }
                        ]
                    }
                }
            }
        },
        "role-categories":{
            "316215865-5":{
                "id":"316215865-5",
                "type":"role-categories",
                "attributes":{
                    "kind":"production-and-engineering",
                    "title":"PRODUCȚIE ȘI INGINERIE"
                }
            },
            "1334280149-4":{
                "id":"1334280149-4",
                "type":"role-categories",
                "attributes":{
                    "kind":"performer",
                    "title":"ARTIȘTI"
                }
            },
            "1334280149-5":{
                "id":"1334280149-5",
                "type":"role-categories",
                "attributes":{
                    "kind":"production-and-engineering",
                    "title":"PRODUCȚIE ȘI INGINERIE"
                }
            },
            "556406361-4":{
                "id":"556406361-4",
                "type":"role-categories",
                "attributes":{
                    "kind":"performer",
                    "title":"ARTIȘTI"
                }
            },
            "556406361-3":{
                "id":"556406361-3",
                "type":"role-categories",
                "attributes":{
                    "kind":"composer-and-lyrics",
                    "title":"COMPOZIȚIE ȘI VERSURI"
                }
            },
            "1151491184-4":{
                "id":"1151491184-4",
                "type":"role-categories",
                "attributes":{
                    "kind":"performer",
                    "title":"ARTIȘTI"
                }
            },
            "1151491184-3":{
                "id":"1151491184-3",
                "type":"role-categories",
                "attributes":{
                    "kind":"composer-and-lyrics",
                    "title":"COMPOZIȚIE ȘI VERSURI"
                }
            },
            "1334280149-3":{
                "id":"1334280149-3",
                "type":"role-categories",
                "attributes":{
                    "kind":"composer-and-lyrics",
                    "title":"COMPOZIȚIE ȘI VERSURI"
                }
            },
            "1151491184-5":{
                "id":"1151491184-5",
                "type":"role-categories",
                "attributes":{
                    "kind":"production-and-engineering",
                    "title":"PRODUCȚIE ȘI INGINERIE"
                }
            },
            "556406361-5":{
                "id":"556406361-5",
                "type":"role-categories",
                "attributes":{
                    "kind":"production-and-engineering",
                    "title":"PRODUCȚIE ȘI INGINERIE"
                }
            },
            "316215865-3":{
                "id":"316215865-3",
                "type":"role-categories",
                "attributes":{
                    "kind":"composer-and-lyrics",
                    "title":"COMPOZIȚIE ȘI VERSURI"
                }
            },
            "316215865-4":{
                "id":"316215865-4",
                "type":"role-categories",
                "attributes":{
                    "kind":"performer",
                    "title":"ARTIȘTI"
                }
            }
        },
        "lyrics":{
            "316215865":{
                "id":"316215865",
                "type":"lyrics",
                "attributes":{
                    "ttml":"<tt xmlns=\"http://www.w3.org/ns/ttml\" xmlns:itunes=\"http://music.apple.com/lyric-ttml-internal\" xmlns:ttm=\"http://www.w3.org/ns/ttml#metadata\" itunes:timing=\"Line\" xml:lang=\"en\"><head><metadata><ttm:agent type=\"person\" xml:id=\"v1\"><ttm:name type=\"full\">OceanLab</ttm:name></ttm:agent><iTunesMetadata xmlns=\"http://music.apple.com/lyric-ttml-internal\" leadingSilence=\"0.000\"><songwriters><songwriter>Jono Grant</songwriter><songwriter>Justine Suissa</songwriter><songwriter>Paavo Siljamäki</songwriter><songwriter>Tony McGuinness</songwriter></songwriters></iTunesMetadata></metadata></head><body dur=\"07:27.53\"><div begin=\"02:04.343\" end=\"02:31.626\" itunes:songPart=\"Verse\"><p begin=\"02:04.343\" end=\"02:10.995\" ttm:agent=\"v1\">My love is like footsteps in the snow, baby</p><p begin=\"02:10.995\" end=\"02:16.568\" ttm:agent=\"v1\">I follow you everywhere you go, baby</p><p begin=\"02:16.568\" end=\"02:20.632\" ttm:agent=\"v1\">The painless light has come to wake you</p><p begin=\"02:20.632\" end=\"02:23.708\" ttm:agent=\"v1\">But you will never realize</p><p begin=\"02:23.708\" end=\"02:31.626\" ttm:agent=\"v1\">That I inspire the dreams that guide you, baby</p></div><div begin=\"02:31.626\" end=\"02:59.56\" itunes:songPart=\"Verse\"><p begin=\"02:31.626\" end=\"02:38.453\" ttm:agent=\"v1\">I\\'ll follow the winds that bring the cold, baby</p><p begin=\"02:38.453\" end=\"02:44.177\" ttm:agent=\"v1\">I\\'ll light a fire in your soul, baby</p><p begin=\"02:44.177\" end=\"02:47.95\" ttm:agent=\"v1\">The lightest touch of feathers falling</p><p begin=\"02:47.95\" end=\"02:51.27\" ttm:agent=\"v1\">My love may be invisible</p><p begin=\"02:51.27\" end=\"02:59.56\" ttm:agent=\"v1\">But I inspire the dreams that guide you, baby</p></div><div begin=\"02:59.56\" end=\"03:27.575\" itunes:songPart=\"Verse\"><p begin=\"02:59.56\" end=\"03:04.184\" ttm:agent=\"v1\">You\\'re half a world away</p><p begin=\"03:06.77\" end=\"03:13.387\" ttm:agent=\"v1\">But in my mind, I whisper every single word you say</p><p begin=\"03:13.387\" end=\"03:17.848\" ttm:agent=\"v1\">And before you sleep at night</p><p begin=\"03:20.249\" end=\"03:27.575\" ttm:agent=\"v1\">You pray to me, your lucky star, your singing satellite</p></div><div begin=\"03:51.282\" end=\"03:55.543\" itunes:songPart=\"Verse\"><p begin=\"03:51.282\" end=\"03:55.543\" ttm:agent=\"v1\">Your singing satellite</p></div><div begin=\"04:04.738\" end=\"04:08.883\" itunes:songPart=\"Verse\"><p begin=\"04:04.738\" end=\"04:08.883\" ttm:agent=\"v1\">Your satellite</p></div><div begin=\"04:22.118\" end=\"04:49.855\" itunes:songPart=\"Verse\"><p begin=\"04:22.118\" end=\"04:26.344\" ttm:agent=\"v1\">You\\'re half a world away</p><p begin=\"04:28.922\" end=\"04:35.714\" ttm:agent=\"v1\">But in my mind, I whisper every single word you say</p><p begin=\"04:35.714\" end=\"04:38.886\" ttm:agent=\"v1\">And before you sleep at night</p><p begin=\"04:42.587\" end=\"04:49.855\" ttm:agent=\"v1\">You pray to me, your lucky star, your singing satellite</p></div><div begin=\"05:16.685\" end=\"05:45.525\" itunes:songPart=\"Verse\"><p begin=\"05:16.685\" end=\"05:23.988\" ttm:agent=\"v1\">You\\'re half a world away</p><p begin=\"05:23.988\" end=\"05:30.548\" ttm:agent=\"v1\">But in my mind, I whisper every single word you say</p><p begin=\"05:30.548\" end=\"05:37.409\" ttm:agent=\"v1\">And before you sleep at night</p><p begin=\"05:37.409\" end=\"05:45.525\" ttm:agent=\"v1\">You pray to me, your lucky star, your singing satellite</p></div><div begin=\"05:54.696\" end=\"05:59.491\" itunes:songPart=\"Verse\"><p begin=\"05:54.696\" end=\"05:59.491\" ttm:agent=\"v1\">Your singing satellite</p></div></body></tt>",
                    "playParams":{
                        "id":"WE_317878790",
                        "kind":"lyric",
                        "catalogId":"316215865",
                        "displayType":2
                    }
                }
            },
            "556406361":{
                "id":"556406361",
                "type":"lyrics",
                "attributes":{
                    "ttml":"<tt xmlns=\"http://www.w3.org/ns/ttml\" xmlns:itunes=\"http://music.apple.com/lyric-ttml-internal\" itunes:timing=\"Line\" xml:lang=\"en\"><head><metadata><iTunesMetadata xmlns=\"http://music.apple.com/lyric-ttml-internal\"><songwriters><songwriter>Yuri Kane</songwriter></songwriters></iTunesMetadata></metadata></head><body dur=\"00:05:17.320\"><div begin=\"00:01:48.620\" end=\"00:02:16.620\"><p begin=\"00:01:48.620\" end=\"00:01:54.010\">Was wrong to say I wouldn\\'t change a 
thing</p><p begin=\"00:01:54.010\" end=\"00:02:02.510\">\\'Cause in the story of our lives, the best of times through color glass</p><p begin=\"00:02:02.510\" end=\"00:02:05.140\">And if you should call</p><p begin=\"00:02:05.140\" end=\"00:02:09.060\">It\\'s no trouble, no trouble at all</p><p begin=\"00:02:09.060\" end=\"00:02:16.620\">I\\'ll take out the sun, back where we begun again</p></div><div begin=\"00:02:49.920\" end=\"00:03:19.260\"><p begin=\"00:02:49.920\" end=\"00:02:57.120\">Time goes on enough to let me move on past</p><p begin=\"00:02:57.120\" end=\"00:03:05.230\">Every little now and then it creeps on back to shade my smile</p><p begin=\"00:03:05.230\" end=\"00:03:08.010\">I\\'m here once again</p><p begin=\"00:03:08.010\" end=\"00:03:11.770\">And I\\'m dealing and I\\'m feeling a pain</p><p begin=\"00:03:11.770\" end=\"00:03:19.260\">So who takes the fall that covers it all again</p></div><div begin=\"00:03:49.120\" end=\"00:04:19.680\"><p begin=\"00:03:49.120\" end=\"00:03:52.230\">Put it on the right track, get it right back</p><p begin=\"00:03:52.230\" end=\"00:03:56.030\">A message from my heart it\\'s too loud to stay apart</p><p begin=\"00:03:56.030\" end=\"00:03:59.480\">So put it on the right track, steal it right back</p><p begin=\"00:03:59.480\" end=\"00:04:03.750\">It\\'s time, time now</p><p begin=\"00:04:03.750\" end=\"00:04:07.090\">Put it on the right track, get it right back</p><p begin=\"00:04:07.090\" end=\"00:04:10.840\">A message from my heart it\\'s too loud to stay apart</p><p begin=\"00:04:10.840\" end=\"00:04:14.490\">So put it on the right track, steal it right back</p><p begin=\"00:04:14.490\" end=\"00:04:19.680\">It\\'s high time now</p></div><div begin=\"00:04:48.170\" end=\"00:05:17.320\"><p begin=\"00:04:48.170\" end=\"00:04:51.380\">Put it on the right track, get it right back</p><p begin=\"00:04:51.380\" end=\"00:04:55.080\">A message from my heart it\\'s too loud to stay apart</p><p begin=\"00:04:55.080\" end=\"00:04:58.800\">So put it on the right track, steal it right back</p><p begin=\"00:04:58.800\" end=\"00:05:02.730\">It\\'s high time now</p><p begin=\"00:05:02.730\" end=\"00:05:05.970\">Put it on the right track, get it right back</p><p begin=\"00:05:05.970\" end=\"00:05:09.760\">A message from my heart it\\'s too loud to stay apart</p><p begin=\"00:05:09.760\" end=\"00:05:13.860\">So put it on the right track, steal it right back</p><p begin=\"00:05:13.860\" end=\"00:05:17.320\">It\\'s high time now</p></div></body></tt>",
                    "playParams":{
                        "id":"MX_30762598-36006968",
                        "kind":"lyric",
                        "catalogId":"556406361",
                        "displayType":2
                    }
                }
            },
            "1151491184":{
                "id":"1151491184",
                "type":"lyrics",
                "attributes":{
                    "ttml":"<tt xmlns=\"http://www.w3.org/ns/ttml\" xmlns:itunes=\"http://music.apple.com/lyric-ttml-internal\" itunes:timing=\"None\" xml:lang=\"it\"><head><metadata><iTunesMetadata xmlns=\"http://music.apple.com/lyric-ttml-internal\"><songwriters><songwriter>Ferry Corsten</songwriter></songwriters></iTunesMetadata></metadata></head><body><div><p>INSTRUMENTAL</p></div></body></tt>",
                    "playParams":{
                        "id":"MX_14500289",
                        "kind":"lyric",
                        "catalogId":"1151491184",
                        "displayType":1
                    }
                }
            }
        },
        "artists":{
            "44166471":{
                "id":"44166471",
                "type":"artists",
                "href":"/v1/catalog/ro/artists/44166471?l=ro",
                "attributes":{
                    "genreNames":[
                        "Trance"
                    ],
                    "name":"Gouryella",
                    "artwork":{
                        "width":948,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Features124/v4/f6/75/fa/f675fa5f-5041-263b-b552-c15daa46760e/pr_source.png/{w}x{h}bb.{f}",
                        "height":948,
                        "textColor3":"3a3a3a",
                        "textColor2":"2f2f2f",
                        "textColor4":"4f4f4f",
                        "textColor1":"151515",
                        "bgColor":"cecece",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/artist/gouryella/44166471?l=ro"
                }
            },
            "342853516":{
                "id":"342853516",
                "type":"artists",
                "href":"/v1/catalog/ro/artists/342853516?l=ro",
                "attributes":{
                    "genreNames":[
                        "Trance"
                    ],
                    "name":"Yuri Kane",
                    "artwork":{
                        "width":3000,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/a7/fb/89/a7fb89ab-853c-02ea-086f-1456569439c6/8718522327025.png/{w}x{h}ac.{f}",
                        "height":3000,
                        "textColor3":"323300",
                        "textColor2":"2d2e00",
                        "textColor4":"565800",
                        "textColor1":"000000",
                        "bgColor":"fcff00",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/artist/yuri-kane/342853516?l=ro"
                }
            },
            "562637194":{
                "id":"562637194",
                "type":"artists",
                "href":"/v1/catalog/ro/artists/562637194?l=ro",
                "attributes":{
                    "genreNames":[
                        "Trance"
                    ],
                    "name":"Jeremy Vancaulart",
                    "artwork":{
                        "width":2400,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music49/v4/99/89/59/9989592b-83aa-370e-f72b-29fe52930183/8718525083287.png/{w}x{h}ac.{f}",
                        "height":2400,
                        "textColor3":"313131",
                        "textColor2":"2c2c2c",
                        "textColor4":"4f4f4f",
                        "textColor1":"060606",
                        "bgColor":"dfdfdf",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/artist/jeremy-vancaulart/562637194?l=ro"
                }
            },
            "3688902":{
                "id":"3688902",
                "type":"artists",
                "href":"/v1/catalog/ro/artists/3688902?l=ro",
                "attributes":{
                    "genreNames":[
                        "Trance"
                    ],
                    "name":"Ferry Corsten",
                    "artwork":{
                        "width":1200,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Features115/v4/72/e5/0e/72e50e63-3518-a5cd-6710-0744a51ec162/mzl.satfpuzg.jpg/{w}x{h}bb.{f}",
                        "height":1200,
                        "textColor3":"313131",
                        "textColor2":"171717",
                        "textColor4":"404040",
                        "textColor1":"040404",
                        "bgColor":"e6e6e6",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/artist/ferry-corsten/3688902?l=ro"
                }
            },
            "18214657":{
                "id":"18214657",
                "type":"artists",
                "href":"/v1/catalog/ro/artists/18214657?l=ro",
                "attributes":{
                    "genreNames":[
                        "Dance"
                    ],
                    "name":"OceanLab",
                    "artwork":{
                        "width":788,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Features124/v4/ab/d8/a5/abd8a539-0898-a481-3b63-40f688876d68/pr_source.png/{w}x{h}bb.{f}",
                        "height":787,
                        "textColor3":"2f2c2b",
                        "textColor2":"1f1b1a",
                        "textColor4":"393635",
                        "textColor1":"110d0c",
                        "bgColor":"a5a5a5",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/artist/oceanlab/18214657?l=ro"
                }
            }
        },
        "albums":{
            "556406001":{
                "id":"556406001",
                "type":"albums",
                "href":"/v1/catalog/ro/albums/556406001?l=ro",
                "attributes":{
                    "copyright":"℗ 2012 Lange Recordings",
                    "genreNames":[
                        "Dance",
                        "Muzică"
                    ],
                    "releaseDate":"2012-09-11",
                    "isMasteredForItunes":false,
                    "upc":"5052653379946",
                    "artwork":{
                        "width":2400,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/v4/70/ff/41/70ff41e6-faf8-de2f-764c-5243891bc8dc/cover.jpg/{w}x{h}bb.{f}",
                        "height":2400,
                        "textColor3":"c28363",
                        "textColor2":"daa170",
                        "textColor4":"b4865d",
                        "textColor1":"eb9d78",
                        "bgColor":"1d1a11",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"556406001",
                        "kind":"album"
                    },
                    "url":"https://music.apple.com/ro/album/lange-presents-intercity-100/556406001?l=ro",
                    "recordLabel":"Lange Recordings",
                    "trackCount":50,
                    "isCompilation":false,
                    "isPrerelease":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "isSingle":false,
                    "name":"Lange Presents Intercity 100",
                    "artistName":"Various Artists",
                    "isComplete":true
                }
            },
            "1334280142":{
                "id":"1334280142",
                "type":"albums",
                "href":"/v1/catalog/ro/albums/1334280142?l=ro",
                "attributes":{
                    "copyright":"℗ 2018 Black Sunset Music under exclusive license to Armada Music B.V.",
                    "genreNames":[
                        "Trance",
                        "Muzică",
                        "Dance"
                    ],
                    "releaseDate":"2018-01-26",
                    "isMasteredForItunes":false,
                    "upc":"8718522184888",
                    "artwork":{
                        "width":3000,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music118/v4/73/a9/da/73a9daa1-c9f1-9e5f-f9ca-be5b99a36319/8718522184888.png/{w}x{h}bb.{f}",
                        "height":3000,
                        "textColor3":"272c28",
                        "textColor2":"161616",
                        "textColor4":"2b2e29",
                        "textColor1":"111316",
                        "bgColor":"808e74",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/album/hurt-feat-danyka-nadeau-single/1334280142?l=ro",
                    "playParams":{
                        "id":"1334280142",
                        "kind":"album"
                    },
                    "recordLabel":"Black Sunset Music",
                    "isCompilation":false,
                    "trackCount":1,
                    "isPrerelease":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "isSingle":true,
                    "name":"Hurt (feat. Danyka Nadeau) - Single",
                    "artistName":"Jeremy Vancaulart",
                    "isComplete":true
                }
            },
            "316215796":{
                "id":"316215796",
                "type":"albums",
                "href":"/v1/catalog/ro/albums/316215796?l=ro",
                "attributes":{
                    "copyright":"℗ 2009 Anjunabeats",
                    "genreNames":[
                        "Dance",
                        "Muzică",
                        "Muzică electronică"
                    ],
                    "releaseDate":"2009-06-08",
                    "isMasteredForItunes":false,
                    "upc":"5039060138694",
                    "artwork":{
                        "width":1780,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music/31/65/6b/mzi.navynbso.jpg/{w}x{h}bb.{f}",
                        "height":1780,
                        "textColor3":"789ba6",
                        "textColor2":"7cb4ca",
                        "textColor4":"6792a3",
                        "textColor1":"90c0ce",
                        "bgColor":"170908",
                        "hasP3":false
                    },
                    "url":"https://music.apple.com/ro/album/above-beyond-presents-oceanlab-sirens-of-the-sea-remixed/316215796?l=ro",
                    "playParams":{
                        "id":"316215796",
                        "kind":"album"
                    },
                    "recordLabel":"Anjunabeats",
                    "isCompilation":false,
                    "trackCount":25,
                    "isPrerelease":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "isSingle":false,
                    "name":"Above & Beyond Presents OceanLab Sirens of the Sea REMIXED",
                    "artistName":"OceanLab",
                    "isComplete":true
                }
            },
            "1151490543":{
                "id":"1151490543",
                "type":"albums",
                "href":"/v1/catalog/ro/albums/1151490543?l=ro",
                "attributes":{
                    "copyright":"℗ 2016 Armada Music B.V.",
                    "genreNames":[
                        "Trance",
                        "Muzică",
                        "Dance"
                    ],
                    "releaseDate":"2016-09-30",
                    "isMasteredForItunes":false,
                    "upc":"8718522112805",
                    "artwork":{
                        "width":3000,
                        "url":"https://is1-ssl.mzstatic.com/image/thumb/Music123/v4/95/7d/f5/957df58d-e948-8666-3b90-c9362062e25d/8718522112805.png/{w}x{h}bb.{f}",
                        "height":3000,
                        "textColor3":"d3d2d2",
                        "textColor2":"fba117",
                        "textColor4":"d08819",
                        "textColor1":"ffffff",
                        "bgColor":"252120",
                        "hasP3":false
                    },
                    "playParams":{
                        "id":"1151490543",
                        "kind":"album"
                    },
                    "url":"https://music.apple.com/ro/album/a-state-of-trance-15-years/1151490543?l=ro",
                    "recordLabel":"Armada Music Bundles",
                    "isCompilation":false,
                    "trackCount":45,
                    "isPrerelease":false,
                    "audioTraits":[
                        "lossless",
                        "lossy-stereo"
                    ],
                    "isSingle":false,
                    "name":"A State of Trance - 15 Years",
                    "artistName":"Armin van Buuren",
                    "isComplete":false
                }
            }
        }
    }
}
"""
def parse_data(data):
    media = {}
    media_list = []

    print(data)
    id        = data["data"][0]["id"]
    resources = data["resources"]
    playlist  = resources["library-playlists"][id]
    library   = resources["library-songs"]
    attr      = playlist["attributes"]
    relations = playlist["relationships"]["tracks"]["data"]

    media["dir"] = parse.sanitize(
        "{} [{}]".format(
            attr["name"],
            id
        )
    )

    # Apple Music GUI shows an 'aggregated' cover consisting of the first four artworks of the playlist.
    # This is not yet implemented here, we just pick the first artwork and use that.
    # TODO: download the first four artworks and merge them into one picture
    coverArtwork = library[relations[0]["id"]]["attributes"]["artwork"]

    media["coverUrl"] = coverArtwork["url"].format(
        w=coverArtwork["width"],
        h=coverArtwork["height"],
        f="jpg"
    )

    for relation in relations:
        lib_entry = library[relation["id"]]
        lib_rel = lib_entry["relationships"]["catalog"]["data"][0]
        item_type = lib_rel["type"]
        song_id = lib_rel["id"]

        song_entry = resources[item_type][song_id]
        song_rels = song_entry["relationships"]
        song_attr = song_entry["attributes"]

        album_id = song_rels["albums"]["data"][0]["id"]
        album_attr = resources["albums"][album_id]["attributes"]

        filename = parse.sanitize(
            "{} - {}{}".format(
                str(song_attr.get("trackNumber")).zfill(2),
                song_attr.get("name"),
                " [E]" if song_attr.get("contentRating") == "explicit" else ""
            )
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

            "copyright": album_attr.get("copyright"),
            "upc": album_attr.get("upc"),
            "recordlabel": album_attr.get("recordLabel"),
            "trackcount": album_attr.get("trackCount"),
            "album": album_attr.get("name"),
            "albumartist": album_attr.get("artistName"),
        }

        # -- TODO parse song credits

        if song_attr.get('hasLyrics') and song_attr['hasLyrics'] and "lyrics" in song_rels:
            if song_rels["lyrics"].get("data"):
                lyrics_rel = song_rels["lyrics"]["data"][0]
                lyrics_array = resources.get(lyrics_rel["type"])

                if lyrics_array:
                    lyrics_entry = lyrics_array[lyrics_rel["id"]]

                    if lyrics_entry and lyrics_entry.get("attributes"):
                        s.update(
                            lyrics.parse(
                                lyrics_entry["attributes"]["ttml"]
                            )
                        )

        if item_type == "songs":
            s["type"] = 1
        elif item_type == "music-videos":
            s["type"] = 6

        media_list.append(
            parse.opt(s)
        )

    media["tracks"] = media_list
    return media
