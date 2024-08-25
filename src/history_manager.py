# /usr/bin/python
import os
import shutil


from sqlite3 import *

from dotenv import load_dotenv
load_dotenv()

def init_db():
    db = Connection('data/history.db', autocommit=False)
    curse = db.cursor()
    curse.execute('CREATE TABLE IF NOT EXISTS "history" ("nom"	TEXT, "écoutes"	INTEGER, "url"	TEXT, "file"	TEXT)')
    db.commit()
    db.close()

def db_add_entry(name: str, url: str, file: str, curse: Cursor):
    curse.execute(f"INSERT INTO history (nom, écoutes, url, file) VALUES (%s, 1, %s, %s)", (name, url, file))


def try_fetch(name: str, url: str):
    if not os.path.isfile("data/history.db"):
        init_db()
    
    db = Connection('data/history.db', autocommit=False)
    curse = db.cursor()

    curse.execute(f"SELECT écoutes, file FROM history WHERE nom=%s", (name))
    db_entries_with_name = curse.fetchall()

    if db_entries_with_name !=[] and db_entries_with_name[0][1] != '': # the file is in the db
        curse.execute(f"UPDATE history SET écoutes=%s WHERE nom=%s", db_entries_with_name[0][0]+1, name)
        db.commit()
        file = f"data/{db_entries_with_name[0][1]}"
    else:
        curse.execute(f"SELECT écoutes, file FROM history WHERE file!=''")
        cached_songs = curse.fetchall() # gets all the cached songs

        if len(cached_songs)<10:
            # if the cache still isn't full
            worst_file = f"song{len(cached_songs)}.mp3"

            if db_entries_with_name == []: # completely new song
                db_add_entry(name, url, worst_file, curse)
            else: # the file is in the db but not in cache
                curse.execute(f"UPDATE history SET file=%s, écoutes=%s WHERE nom=%s", worst_file, db_entries_with_name[0][0]+1, name)
        else:
            worst_ecoute = cached_songs[0][0]
            worst_file = cached_songs[0][1]

            for i in range(len(db_entries_with_name)):
                if cached_songs[i][0] < worst_ecoute:
                    worst_ecoute = cached_songs[i][0]
                    worst_file = cached_songs[i][1]
                # we found the filename

            curse.execute(f"UPDATE history SET file='' WHERE file=%s", worst_file)
            if db_entries_with_name == []:
                db_add_entry(name, url, worst_file, curse)
            else:
                curse.execute(f"UPDATE history SET file=%s, écoutes=%s WHERE nom=%s", worst_file, db_entries_with_name[0][0]+1, name)
        
        file = f"data/{worst_file}"
        if os.path.isfile(file):
            shutil.move(file,  "temp")

        has_downloaded = os.system(f'{os.environ["YTDLP_PATH"]} -x --audio-format mp3 --audio-quality 0 "{name}" --ffmpeg-location "{os.environ["FFMPEG_PATH"]}" -o "{file}"')
        if has_downloaded==1:
            # download has failed on the yt-dlp side, revert changes made to the db and restore temp file
            if os.path.isfile("temp"):
                shutil.move("temp",  file)
            db.rollback()
        else:
            if os.path.isfile("temp"):
                os.remove("temp")
            db.commit()
    db.close()
    return file
