import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC
from UtaNet_manager import search_lyrics_from_query, get_lyrics_from_lyrics_page


def get_song_info(path):
    tags = EasyID3(path)
    title = tags['title']
    artist = tags['artist']
    # lang = tags['language']
    # print()

    return title[0], artist[0]


def get_all_songs_path(dir):
    songs = os.listdir(dir)
    songs_path = []
    for song in songs:
        songs_path.append(os.path.join(dir, song))

    return songs_path


def mount_lyrics(lyrics, path):
    tags = ID3(path)
    # tags['unsyncedlyrics'] = lyrics
    tags[u"USLT::'eng'"] = (USLT(encoding=3, lang='eng', desc=u'desc', text=lyrics))
    tags.save()


if __name__ == '__main__':
    songs_path = get_all_songs_path('data')
    for song in songs_path:
        print(song)
        title, artist = get_song_info(song)
        url, min_dist = search_lyrics_from_query(title, artist)
        lyrics = get_lyrics_from_lyrics_page(url)
        mount_lyrics(lyrics, song)

        print(lyrics + '\n')
