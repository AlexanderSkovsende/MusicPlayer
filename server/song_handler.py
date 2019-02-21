from collections import deque
import pafy
import vlc
import requests
import re
from time import time
import html


class Song:
    def __init__(self, url, title, duration):
        self.url = url
        self.title = html.escape(title)
        self.duration = duration


class Queue:

    def __init__(self, sio):
        self.sio = sio
        self.q = deque()
        self.escape = set('&?%/=+:;,#$@')
        self.current = None
        self.next_skip = 0

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_fullscreen(True)
        self.set_volume(50)

    def next(self):

        if len(self.q):
            song = self.q.popleft()
            self.current = song
            self.sio.emit('update', self.get_update_data())

            media = self.instance.media_new(song.url)
            media.get_mrl()
            self.player.set_media(media)
            self.player.play()
            self.next_skip = time() + song.duration + 3
        else:
            if self.current is not None:
                self.player.stop()
                self.next_skip = 0
                self.current = None
                self.sio.emit('update', self.get_update_data())

    def add(self, name):
        url = self.search(name)
        video = pafy.new(url)

        best = video.getbest()

        self.q.append(Song(best.url, video.title, video.length))
        self.sio.emit('update', self.get_update_data())

    def search(self, query):

        url = "https://www.youtube.com/results?search_query="

        for char in query:
            if char in self.escape:
                char = "%" + hex(ord(char))[2:]

            url += char

        r = requests.get(url)
        return re.findall(r'/watch\?v=([A-Za-z0-9_\-]{11})', r.text)[0]

    def get_string(self):
        s = ""
        if self.current:
            s += "<font color='darkred'>{}</font><br>".format(self.current.title)

        return s + "<br>".join(song.title for song in self.q)

    def set_volume(self, volume):
        self.volume = volume
        self.player.audio_set_volume(volume)

    def get_update_data(self):
        return {'queue': self.get_string(), 'volume': self.volume}

    def run(self):
        while True:
            if self.next_skip < time():
                self.next()

            self.sio.sleep(0.1)
