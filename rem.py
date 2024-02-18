#!/usr/bin/python

import discord
from discord.ext import commands
import os
import asyncio
import json

from src.quotes import check_integrity, generate_default
from src.music_cog import music_cog

from dotenv import load_dotenv
load_dotenv()


async def setup(bot):
    if not os.path.isfile("data/quotes.json"):
        print("Could not find file 'data/quotes.json'")
        parsed_quotes = generate_default()
    else:
        quotes = open("data/quotes.json", 'r')
        parsed_quotes = json.load(quotes)
        quotes.close()
        
        if not check_integrity(parsed_quotes):
            print("missing fields in quotes.json, using default quotes instead")
            parsed_quotes = generate_default()

    await bot.add_cog(music_cog(bot, parsed_quotes))

def main():
    bot = commands.Bot(command_prefix='rem', intents=discord.Intents.all())
    asyncio.run(setup(bot))
    bot.run(os.environ.get('BOT_TOKEN'))

if __name__=="__main__":
    main()
