# Setup and Installation
## Dependencies
- Install `python3.12` or any newer version 
- Install the pip dependencies by running:

    ```sh
    pip install yt-dlp youtube-search-python discord validators python-dotenv
    pip install -U discord.py[voice]
    ```

- Install [ffmpeg](https://www.ffmpeg.org/download.html)



## Configuration
### Environment
The program needs some environment variables set to be able to run.
You can do so by putting the following in a `.env` file at the root of this repo with the right paths and bot token:
```
FFMPEG_PATH="your/path/to/ffmpeg_exe"
BOT_TOKEN="your_bot_token"
YTDLP_PATH="your/path/to/yt_dlp_exe"
```
The executable for `yt-dlp` should be in the `Scripts`folder of your python installation folder

### Bot customization (optional)
You can customize by user the messages sent by the bot in various contexts by providing a `data/quotes.json` file. It should follow at least the default structure in `src/quotes.py` (especially regarding the `"default"` fields).

For example, say you wanted to specify the bot's response on a `remp` request for user `foo`, the `data/quotes.json` contain:

```json
 {
    "play": {
        "request_recieved": {
            "foo": "This is rem's custom `remp` response for foo."
        }
    },
 }
```

# Launching
To launch the bot, set yourself at the root of this repo and run:

```
python rem.py
```
