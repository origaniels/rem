from os import environ
import discord
import music_cog
from src.history_manager import playlist_add_song, playlist_remove_song, try_fetch

class Playlist:
    def __init__(
            self,
            name: str,
            cog: music_cog.music_cog,
            songs: list[str]
        ) -> None:
        self.name = name
        self.cog = cog
        self.songs = songs
        self.stop_playing = False

    def add_song(self, url: str):
        playlist_add_song(self.name, url)
        self.songs.append(url)

    def remove_song(self, url: str):
        playlist_remove_song(self.name, url)
        self.songs.remove(url)

    def loop(self):
        self.loop = not self.loop

    def play(self):
        # we must already be connected to VC
        while self.loop:
            for song in self.songs.copy():
                if not self.stop_playing:
                    self.play_single_song(song)
        
        self.cog.play_next()

    def play_single_song(self, song: str):
        file = try_fetch(song, song)
        self.cog.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source=file))

    def stop_playing(self):
        # triggers the stop of the playlist after the current song ends
        self.stop_playing = True