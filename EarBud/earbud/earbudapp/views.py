import pymongo
from django.shortcuts import render, HttpResponse
from pip._internal.network.auth import Credentials


from pymongo import MongoClient, WriteConcern, ReadPreference
from pymongo.errors import OperationFailure
from pymongo.read_concern import ReadConcern
from pymongo.server_api import ServerApi


from .forms import AddData
from .forms import RemoveData
from .forms import EditData
from django import forms

def home(request):
    context = {}
    return render(request, "welcome.html", context)

def editData(request):
    add_data = AddData(request.POST or None)
    remove_data = RemoveData(request.POST or None)
    edit_data = EditData(request.POST or None)

    uri = "mongodb+srv://rabreader:BooImAGhost@earbud.k1i71eh.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(uri)

    def add_song(session, form_data):
        song = {
            "artist": form_data["artist"],
            "title": form_data["song_title"],
            "album": form_data["album"],
            "genre": form_data["genre"],
            "releaseYear": form_data["release_year"],
            "songLength": form_data["song_length"]
        }
        session.client['test'].Playlist.insert_one(song, session=session)

    def delete_song(session, form_data):
        song = {
            "artist": form_data["artist"],
            "title": form_data["song_title"],
            "album": form_data["album"],
            "genre": form_data["genre"],
            "releaseYear": form_data["release_year"],
            "songLength": form_data["song_length"]
        }
        session.client['test'].Playlist.delete_one(song, session=session)

    def edit_song(session, form_data):
        songedit = form_data["song_to_edit"]
        artistE = form_data["artist"]
        titleE = form_data["song_title"]
        albumE = form_data["album"]
        genreE = form_data["genre"]
        releaseE = form_data["release_year"]
        timeE = form_data["song_length"]

        collection = session.client['test']['Playlist']
        existing_song = collection.find_one({"title": songedit}, session=session)
        if existing_song:
            update_data = {
                "$set": {
                    "artist": artistE,
                    "title": titleE,
                    "album": albumE,
                    "genre": genreE,
                    "releaseYear": releaseE,
                    "songLength": timeE
                }
            }
            collection.update_one({"title": songedit}, update_data, session=session)
        else:
            raise OperationFailure(f"Song with title '{songedit}' not found.")

    with client.start_session() as session:
        try:
            with session.start_transaction(
                read_concern=ReadConcern("majority"),
                write_concern=WriteConcern(w="majority"),
                read_preference=ReadPreference.PRIMARY,
            ):
                if request.method == "POST":
                    if 'add_song' in request.POST:
                        form = AddData(request.POST)
                        if form.is_valid():
                            add_song(session, form.cleaned_data)
                    if 'delete_song' in request.POST:
                        form = RemoveData(request.POST)
                        if form.is_valid():
                            delete_song(session, form.cleaned_data)
                    if 'edit_song' in request.POST:
                        form = EditData(request.POST)
                        if form.is_valid():
                            edit_song(session, form.cleaned_data)
        except OperationFailure as e:
            context = {'error_message': str(e)}
            return render(request, "errorpage.html", context)

    context = {'form_add_data': add_data, 'form_remove_data': remove_data, 'form_edit_data': edit_data}
    return render(request, "adddata.html", context)

def viewPlaylist(request):
    context = {}
    uri = "mongodb+srv://rabreader:BooImAGhost@earbud.k1i71eh.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['Playlist']
    playlist_data = collection.find({})
    playlist_attributes = []
    for i in playlist_data:
        artist = i.get("artist", "")
        title = i.get("title", "")
        album = i.get("album", "")
        genre = i.get("genre", "")
        release = i.get("releaseYear", "")
        time = i.get("songLength", "")

        playlist_attributes.append({
            "artist": artist,
            "title": title,
            "album": album,
            "genre": genre,
            "releaseYear": release,
            "songLength": time
        })
        context = {'playlist_attributes': playlist_attributes}
    return render(request, "showplaylist.html", context)

def generateReport(request):
    context = {}
    uri = "mongodb+srv://rabreader:BooImAGhost@earbud.k1i71eh.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['test']
    collection = db['Playlist']

    #get top artists
    getTopArtistsPipeline = [
        {"$group": {"_id": "$artist", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$project": {"artist": 1}},
        {"$limit": 4}
    ]
    topArtists = list(collection.aggregate(getTopArtistsPipeline))
    rankedArtists = [f"{i + 1}. {entry['_id']}" for i, entry in enumerate(topArtists)]
    context['ranked_artists'] = "\n".join(rankedArtists)

    #get top genres
    genrePipeline = [
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$project": {"genre": 1}},
        {"$limit": 4}
    ]
    topGenres = list(collection.aggregate(genrePipeline))
    rankedGenres = [f"{i + 1}. {entry['_id']}" for i, entry in enumerate(topGenres)]
    context['ranked_genres'] = "\n".join(rankedGenres)

    #top 3 eras
    eras = [
        {"name": "2020s", "start": 2020, "end": 2029},
        {"name": "2010s", "start": 2010, "end": 2019},
        {"name": "2000s", "start": 2000, "end": 2009},
        {"name": "1990s", "start": 1990, "end": 1999},
        {"name": "1980s", "start": 1980, "end": 1989},
        {"name": "1970s", "start": 1970, "end": 1979},
        {"name": "1960s", "start": 1960, "end": 1969},
        {"name": "1950s", "start": 1950, "end": 1959}
    ]
    top3ErasPipeline = [
        {
            "$group": {
                "_id": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {
                                    "$and": [
                                        {"$gte": ["$releaseYear", era["start"]]},
                                        {"$lte": ["$releaseYear", era["end"]]}
                                    ]
                                },
                                "then": era["name"]
                            } for era in eras
                        ],
                        "default": "Other"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$project": {"name": "$_id"}},
        {"$limit": 3}
    ]

    top3Eras = list(collection.aggregate(top3ErasPipeline))
    rankedEras = [f"{i + 1}. {entry['_id']}" for i, entry in enumerate(top3Eras)]
    context['top_3_eras'] = "\n".join(rankedEras)

    #average song length
    averageSongLengthPipeline = [
        {
            "$group": {
                "_id": None,
                "totalSeconds": {
                    "$sum": {
                        "$add": [{"$multiply": [{"$toInt": {"$arrayElemAt": [{"$split": ["$songLength", ":"]}, 0]}},60]},
                            {"$toInt": {"$arrayElemAt": [{"$split": ["$songLength", ":"]}, 1]}}
                        ]
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "averageSeconds": {"$divide": ["$totalSeconds", "$count"]}
            }
        },
        {
            "$project": {
                "averageSongLength": {
                    "$concat": [
                        {
                            "$toString": {
                                "$cond": [
                                    {"$gte": ["$averageSeconds", 600]},
                                    {"$floor": {"$divide": ["$averageSeconds", 60]}},
                                    {"$concat": [{"$toString": {"$floor": {"$divide": ["$averageSeconds", 60]}}}]}
                                ]
                            }
                        }, ":",
                        {
                            "$cond": [
                                {"$gte": [{"$mod": [{"$toInt": "$averageSeconds"}, 60]}, 10]},
                                {"$toString": {"$mod": [{"$toInt": "$averageSeconds"}, 60]}},
                                {"$concat": ["0", {"$toString": {"$mod": [{"$toInt": "$averageSeconds"}, 60]}}]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]
    averageSongLength = list(collection.aggregate(averageSongLengthPipeline))
    context['average_song_length'] = averageSongLength[0].get('averageSongLength', '')

    #get recs
    recommendations_pipeline = [
            {"$sample": {"size": 3}},
            {
                "$group": {
                    "_id": "$genre",
                    "songs": {
                        "$push": {
                            "artist": "$artist",
                            "title": "$title",
                            "album": "$album",
                            "genre": "$genre"
                        }
                    }
                }
            },
            {
                "$lookup": {
                    "from": "Recs",
                    "localField": "_id",
                    "foreignField": "genre",
                    "as": "recommendations"
                }
            },
            {"$unwind": "$recommendations"},
            {"$replaceRoot": {"newRoot": "$recommendations"}},
            {
                "$project": {
                    "_id": 0,
                    "artist": "$artist",
                    "title": "$title",
                    "album": "$album",
                    "genre": "$genre"
                }
            },
            {"$limit": 3}
        ]
    recommendations = list(collection.aggregate(recommendations_pipeline))
    recommendationsFormatted = [
        {
            "artist": entry.get("artist"),
            "title": entry.get("title"),
            "album": entry.get("album"),
            "genre": entry.get("genre")
        }
        for entry in recommendations
    ]

    context['recommendations'] = recommendationsFormatted



    return render(request, "generatereport.html", context)






# Create your views here.
