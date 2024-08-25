import discord
from discord.ext import commands
import random
from validators import url
from os import environ

#from youtube_dl import YoutubeDL
from youtubesearchpython import *
from src.history_manager import *
from dotenv import load_dotenv

load_dotenv()


class music_cog(commands.Cog):
    def __init__(self, bot, quotes: dict):
        self.bot = bot
    
        self.quotes = quotes

        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.loop = False
        self.queue_out = [] #stores last played song
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.randy = 0
        self.count = 0
        self.ctx = None

        self.vc: discord.VoiceClient = None


     #searching the item on youtube
    def search(self, query):    
        customSearch = CustomSearch(query,SearchMode.videos, limit = 20)
        i=0
        name=customSearch.result()['result'][i]['title']
        s1='EXTENDED'
        s2='extended'
        s3='Extended'
        while s1 in name or s2 in name or s3 in name:
            i += 1
            name = customSearch.result()['result'][i]['title']
        url = customSearch.result()['result'][i]['link']

        return url

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            name = self.music_queue[0][0]
            file = try_fetch(name, name)
            self.randy = random.randint(1,10000)
            if self.randy==10:
                if self.loop == False:
                    self.queue_out = [self.music_queue.pop(0)]
                    self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source="../data/WHAT_IS_EUUUH.mp3"), after=lambda e: self.play_next())
                else :
                    self.queue_out = [self.music_queue[0]]
                    self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source="../data/WHAT_IS_EUUUH.mp3"), after=lambda e: self.play_next())
                    
            else:
                if self.loop == False:
                    self.queue_out = [self.music_queue.pop(0)]

                    try:
                        self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source=file), after=lambda e: self.play_next())
                    except discord.errors.ClientException:
                        self.vc.stop()
                        self.music_queue = self.queue_out + self.music_queue
                        self.play_next()
                else:
                    self.queue_out = [self.music_queue[0]]
                    self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source=file), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        self.randy = random.randint(1,10000)
        if len(self.music_queue) > 0:
            self.is_playing = True
            name = self.music_queue[0][0]
            file = try_fetch(name, name)
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            #remove the first element as you are currently playing it
            if self.randy == 10:
                if self.loop == False:
                    self.queue_out = [self.music_queue.pop(0)]
                    try:
                        self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source= "WHAT_IS_EUUUH.mp3"), after=lambda e: self.play_next())
                    except discord.errors.ClientException:
                        with open('data/rem.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(file=picture)
                        await self.play_music()
                else :
                    self.queue_out = [self.music_queue[0]]
                    try:
                        self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source= "WHAT_IS_EUUUH.mp3"), after=lambda e: self.play_next())
                    except discord.errors.ClientException:
                        with open('data/rem.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(file=picture)
                        await self.play_music()
            else:
                if self.loop == False:
                    self.queue_out = [self.music_queue.pop(0)]
                    try:
                        
                        self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source= file), after=lambda e: self.play_next())
                    except discord.errors.ClientException:
                        with open('data/rem.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(file=picture)
                        self.music_queue.insert(0, self.queue_out[-1])
                        self.vc.skip()
                        await self.play_music(ctx)
                else:
                    self.queue_out = [self.music_queue[0]]
                    try:
                        self.vc.play(discord.FFmpegPCMAudio(executable=environ['FFMPEG_PATH'], source= file), after=lambda e: self.play_next())
                    except discord.errors.ClientException:
                        with open('data/rem.png', 'rb') as f:
                            picture = discord.File(f)
                            await ctx.send(file=picture)
                        self.vc.stop()
                        await self.play_music(ctx)
        else:
            self.is_playing = False

    @commands.command(name="p", aliases=["playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        self.ctx = ctx
        voice_channel = ctx.author.voice.channel
        authorname = str(ctx.author)
        if voice_channel is None:
            if authorname in self.quotes["complaints"]:
                complainlist: list[str] = self.quotes["complaints"][authorname]
            else:
                complainlist: list[str] = self.quotes["complaints"]["default"]

            i=self.count
            if i >= len(complainlist):
                i = len(complainlist)-1
            await ctx.send(complainlist[i].replace("__PLACEHOLDER_USERNAME__", authorname))
            self.count += 1
        else:
            if "list=" in query:
                await send_message(ctx, self.quotes["play"]["bad_request"])
            else:
                if url(query):
                    song = query
                else:
                    song = self.search(query)
                if type(song) == type(True):
                    await send_message(ctx, self.quotes["play"]["song_error"])

                elif song in self.quotes["play"]["special_urls"]:
                    await ctx.send(self.quotes["play"]["special_urls"][song])
                else:
                    await send_message(ctx, self.quotes["play"]["request_recieved"], song)
                    self.music_queue.append([song, voice_channel])
                    
                    if self.is_playing == False:
                        await self.play_music(ctx)

    @commands.command(name="loop", help="turns on loop")
    async def loop(self, ctx):
        if self.loop == True:
            self.loop = False
            if self.music_queue != []:
                self.music_queue = self.music_queue[1:]
            await send_message(ctx, self.quotes["loop"]["loop_off"])
        else:
            self.loop = True
            if len(self.queue_out) > 0 and self.is_playing:
                self.music_queue = [self.queue_out[0]] + self.music_queue
            await send_message(ctx, self.quotes["loop"]["loop_on"])

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        self.ctx = ctx
        if self.vc != None and self.vc:
            ctx.voice_client.stop()
            if self.loop:
                if len(self.music_queue) > 0:
                    self.music_queue = self.music_queue[1:]
                else:
                    self.music_queue = []
            #try to play next in the queue if it exists
            


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        if len(self.music_queue)>0:
            await send_message(ctx, self.quotes["queue"]["not_empty_queue"])
            
            for i in range(0, len(self.music_queue)):
                await ctx.send(self.music_queue[i][0])
            
            await send_message(ctx, self.quotes["queue"]["after"])
        else:
            await send_message(ctx, self.quotes["queue"]["empty_queue"])

    @commands.command(name="leave", aliases=["disconnect", "l", "dis"], help="Kick the bot from VC")
    async def dis(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

    @commands.command(name="sleep", aliases=["sl"], help="Kick the bot from VC")
    async def sleep(self, ctx):
        await send_message(ctx, self.quotes["sleep"])

        self.is_playing = False
        self.is_paused = False
        await ctx.bot.close()

async def send_message(ctx, message_dict: dict[str, str], song=""):
    authorname = str(ctx.author)
    if authorname in message_dict:
        message = message_dict[authorname].replace("__PLACEHOLDER_USERNAME__", authorname).replace("__PLACEHOLDER_SONG__", song)
    else:
        message = message_dict["default"].replace("__PLACEHOLDER_USERNAME__", authorname).replace("__PLACEHOLDER_SONG__", song)
    await ctx.send(message)

