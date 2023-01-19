import spotipy, time, asyncio, random,
from spotipy.oauth2 import SpotifyOAuth
from kasa import SmartBulb

cid = 'CLIENT_ID'
secret = 'SECRET_ID'
redirect_uri = "REDIRECT_URL"
scope = "user-read-currently-playing"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                               client_secret=secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
current_song_id = ""
start_time = ""

async def color(rhue):
    bulb = SmartBulb("")
    run_once = 0
    if run_once == 0:
        await bulb.update()
        run_once = 1
    await bulb.set_hsv(rhue, 100, 100, transition=0)
    #print(bulb.hsv)

import spotipy, time, asyncio, random,
from spotipy.oauth2 import SpotifyOAuth
from kasa import SmartBulb

cid = 'CLIENT_ID'
secret = 'SECRET_ID'
redirect_uri = "REDIRECT_URL"
scope = "user-read-currently-playing"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                               client_secret=secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
current_song_id = ""
start_time = ""

async def color(rhue):
    bulb = SmartBulb("DEVICE_IP")
    run_once = 0
    if run_once == 0:
        await bulb.update()
        run_once = 1
    await bulb.set_hsv(rhue, 100, 100, transition=0)
    #print(bulb.hsv)

def timer():
    global start_time
    start_time = time.time()

def get_current_song():
    global current_song_id
    track = spotify.current_playback()
    track_position = track['progress_ms']
    offset = (track_position / 1000)
    artist = track["item"]["artists"][0]["name"]
    t_name = track["item"]["name"]
    t_id = track["item"]["id"]
    if t_id != current_song_id:
        print(f"Currently playing {artist} - {t_name} - {t_id}")
        current_song_id = t_id
        timer()
    return t_id, offset

def get_audio_data(t_id):
    audio_analysis = spotify.audio_analysis(t_id)
    beats = audio_analysis["beats"]
    song_length = format(audio_analysis["track"]["duration"], '.2f')
    beat_list = list(map(lambda x: x["start"], beats))
    return beat_list, song_length

def get_beats(beat_list, t_id, start_time, song_length, offset):
    global current_song_id
    T_stamp = ['%.2f' % beat for beat in beat_list]
    while t_id == current_song_id:
        elapsed_time = format((time.time() - start_time + offset), '.2f')
        if elapsed_time >= song_length or t_id != current_song_id:
            break
        for elapsed_time in T_stamp:
            rhue = random.randint(0, 360)
            asyncio.run(color(rhue))
            break

def loop():
    global start_time, current_song_id
    t_id, offset = get_current_song()
    if t_id == current_song_id:
        beat_list, song_length = get_audio_data(t_id)
        get_beats(beat_list, t_id, start_time, song_length, offset)

while True:
    loop()
