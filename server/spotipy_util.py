from pprint import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

clientid = '2b4bba8dba4d406a8086f33b644ddcd0'
clientsecret = 'dc13827b3900467383a12e803b10e52f'
redirect = 'http://localhost'
username = 'fabio_ellena'

#necessary to create/add track to public spotify
scope = 'playlist-modify-public'

#get token if cached, otherwise refresh, or generate new prompting to user
token = util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientsecret,redirect_uri=redirect)
sp = spotipy.Spotify(auth=token)
sp.trace = False


def get_playlists_dict(username=username):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists(username)
    playlist_dict = {}
    
    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']
    return playlist_dict


def create_playlist(playlist_name,username=username, sp=sp):
    playlist = sp.user_playlist_create(username, playlist_name)
    pprint(playlist)
    return playlist


def add_tracks(playlist_name,track_ids,username=username):
    sp.user_playlist_add_tracks(username, playlist_name, track_ids)


def get_artist_tracks(artist_name):
    sp = spotipy.Spotify()
    sp.trace = False

    # get matching artist

    results = sp.search(q='artist:' + name, type='artist')
    artists = results['artists']['items']
    artist = None
    if len(artists) == 0:
        return None
    artist = max(artists, key=lambda x: x['popularity'])

    top_tracks = sp.artist_top_tracks(artist['id'], country='FR')['tracks']
    return_tracks = []
    for track in top_tracks:
        return_tracks.append((track['id'], track['name']))
    return return_tracks