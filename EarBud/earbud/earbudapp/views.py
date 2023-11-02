
from django.shortcuts import render, HttpResponse
from pymongo import MongoClient
from pymongo.server_api import ServerApi


from .forms import AddData
from .forms import RemoveData
from django import forms

def home(request):
    add_data = AddData(request.POST or None)
    remove_data = RemoveData(request.POST or None)
    if request.method == "POST":
        if 'add_song' in request.POST:
            form = AddData(request.POST)
            if form.is_valid():
                artist = form.cleaned_data.get("artist")
                title = form.cleaned_data.get("song_title")
                album = form.cleaned_data.get("album")
                genre = form.cleaned_data.get("genre")
                release = form.cleaned_data.get("release_year")
                time = form.cleaned_data.get("song_length")
                uri = "mongodb+srv://rabreader:BooImAGhost@earbud.k1i71eh.mongodb.net/?retryWrites=true&w=majority"
                # Create a new client and connect to the server
                client = MongoClient(uri, server_api=ServerApi('1'))
                db = client['test']
                song = {
                    "artist" : artist,
                    "title" : title,
                    "album" : album,
                    "genre" : genre,
                    "releaseYear": release,
                    "songLength": time
                }
                db.Playlist.insert_one(song)
        if 'delete_song' in request.POST:
            form = RemoveData(request.POST)
            if form.is_valid():
                artist = form.cleaned_data.get("artist")
                title = form.cleaned_data.get("song_title")
                album = form.cleaned_data.get("album")
                genre = form.cleaned_data.get("genre")
                release = form.cleaned_data.get("release_year")
                time = form.cleaned_data.get("song_length")
                uri = "mongodb+srv://rabreader:BooImAGhost@earbud.k1i71eh.mongodb.net/?retryWrites=true&w=majority"
                # Create a new client and connect to the server
                client = MongoClient(uri, server_api=ServerApi('1'))
                db = client['test']
                song = {
                    "artist" : artist,
                    "title" : title,
                    "album" : album,
                    "genre" : genre,
                    "releaseYear" : release,
                    "songLength" : time
                }
                db.Playlist.delete_one(song)
    context = {'form_add_data': add_data, 'form_remove_data': remove_data}
    return render(request, "base.html", context)



# Create your views here.
