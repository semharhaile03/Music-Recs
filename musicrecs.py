import pylast
import requests
import sqlalchemy as db
import pandas as pd

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "c61362683feb81411836a99a40df29e7"  # this is a sample key
API_SECRET = "12b0855c6b5a6f33198e8d818bda7320"

# In order to perform a write operation you need to authenticate yourself
username = "dewytest"
password_hash = pylast.md5("Dewytest04!")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)
choice = input("Would you like to see new recommended tracks or artists? : ")



if choice == "tracks":
    datadf = pd.DataFrame({"Title" : [], "Artist" : []})
    utrack = input("Enter a song title: ")
    uartist = input("Enter the artist of the track: ")
    
    inputtrack = pylast.Track(uartist, utrack, network)
    similar = inputtrack.get_similar(10)
    
    if similar == []:
        print("Sorry, we don't seem to have data on this track.")
    else:
        print("""

        Here are some similiar tracks!:
        """)
        for i in similar:
            track = i.item
            name = track.get_name()
            artist = track.get_artist()
            datadf.loc[len(datadf)] = [str(name), str(artist)]
    
elif choice == "artists":
    datadf = pd.DataFrame({"Artist" : []})
    artist = input("Enter an artist name: ")

    inputartist = pylast.Artist(artist, network)
    similar  = inputartist.get_similar()

    if similar == []:
        print("Sorry, we don't seem to have data on this artist.")
    else:
        print("""

        Here are some similiar artists!:
        """)
        counter = 10
       
        for i in similar:
            artist = i.item
            if counter > 0 and "&" not in str(artist):
                counter -= 1
                datadf.loc[len(datadf)] = [str(artist)]
                    
engine = db.create_engine('sqlite:///datadf.db')
datadf.to_sql("recommended", con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM recommended;")).fetchall()
   print(pd.DataFrame(query_result))

# Now you can use that object everywhere
# track = network.get_track("beabadoobee", "Apple Cider")
# track.love()
# track.add_tags(("awesome", "favorite"))

# print(track)


# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works