from django import forms

class RemoveData(forms.Form):
    artist = forms.CharField(max_length=200)
    song_title = forms.CharField(max_length=200)
    album = forms.CharField(max_length=200)
    genre = forms.CharField(max_length=200)
    release_year = forms.IntegerField()
    song_length = forms.CharField()

class AddData(forms.Form):
    artist = forms.CharField(max_length=200)
    song_title = forms.CharField(max_length=200)
    album = forms.CharField(max_length=200)
    genre = forms.CharField(max_length=200)
    release_year = forms.IntegerField()
    song_length = forms.CharField()

class EditData(forms.Form):
    song_to_edit = forms.CharField(max_length=200)
    artist = forms.CharField(max_length=200)
    song_title = forms.CharField(max_length=200)
    album = forms.CharField(max_length=200)
    genre = forms.CharField(max_length=200)
    release_year = forms.IntegerField()
    song_length = forms.CharField()



