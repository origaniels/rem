def check_integrity(parsed_quotes: dict)->bool:
    # check first key layer
    if not "complaints" in parsed_quotes:
        return False
    complaints = parsed_quotes["complaints"]

    if not "loop" in parsed_quotes:
        return False
    loop = parsed_quotes["loop"]

    if not "play" in parsed_quotes:
        return False
    play = parsed_quotes["play"]

    if not "queue" in parsed_quotes:
        return False
    queue = parsed_quotes["queue"]

    if not "sleep" in parsed_quotes:
        return False
    sleep = parsed_quotes["sleep"]

    #check complaints:
    if not ("default" in complaints and type(complaints["default"])==list):
        return False
    
    #check loop:
    if not ("loop_on" in loop and "loop_off" in loop):
        return False
    if not ("default" in loop["loop_on"] and "default" in loop["loop_off"]):
        return False
    
    #check play:
    if not ("bad_request" in play and "special_urls" in play and "song_error" in play and "request_recieved" in play):
        return False
    if not ("default" in play["bad_request"] and "default" in play["song_error"] and "default" in play["request_recieved"]):
        return False

    #check queue:
    if not ("empty_queue" in queue and "not_empty_queue" in queue and "after" in queue):
        return False
    if not ("default" in queue["empty_queue"] and "default" in queue["not_empty_queue"] and "default" in queue["after"]):
        return False
    
    #check sleep
    if not "default" in sleep:
        return False

    return True

def generate_default()->dict:
    res = {
        "complaints": {
            "default": [
                "Rem needs you to connect to a VoiceChannel to perform her duty __PLACEHOLDER_USERNAME__-sama",
                "Rem really needs you to connect to a VoiceChannel to perform her duty... __PLACEHOLDER_USERNAME__-sama...", 
                "__PLACEHOLDER_USERNAME__-sama...", 
            ]
        },

        "loop": {
            "loop_on": {
                "default": "As you wish __PLACEHOLDER_USERNAME__-sama, songs will now be played in loop.",
            },
            "loop_off": {
                "default": "As you wish __PLACEHOLDER_USERNAME__-sama, songs will no longer be played in loop.",
            }
        },

        "play": {
            "bad_request": {
                "default": "__PLACEHOLDER_USERNAME__-kun seems to have given a bad url. Rem does not support playlists."
            },
            "special_urls": {},
            "song_error": {
                "default": "Could not download, may be a format issue."
            },
            "request_recieved": {
                "default": "It will be done __PLACEHOLDER_USERNAME__-sama. \nThe following song was added to the Queue: __PLACEHOLDER_SONG__"
            }
        },

        "queue": {
            "empty_queue": {
                "default": "Yes __PLACEHOLDER_USERNAME__-sama. There are no songs in queue.",
            },
            "not_empty_queue": {
                "default": "Yes __PLACEHOLDER_USERNAME__-sama, here are the songs in queue:",
            },
            "after": {
                "default": "That is all there is in queue."
            }
        },

        "sleep": {
            "default": "Good night __PLACEHOLDER_USERNAME__-sama."
        }
    }
    
    return res
