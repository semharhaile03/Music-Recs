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


favorites = pd.DataFrame(columns=["Title", "Artist"])
ans = True

while ans:
    choice = input(
        """
Welcome to MusicRecs! Would you like to:
[1] Search for tracks
[2] Search for artists
[3] View your library
[4] Exit
 """)

    if choice == "1":
        utrack = input("Enter a song title: ")
        uartist = input("Enter the artist of the track: ")

        inputtrack = pylast.Track(uartist, utrack, network)

        similar = inputtrack.get_similar(10)
        similartracks = {}

        if similar == []:
            print("Sorry, we don't seem to have data on this track.")
        else:
            print("""

            Here are some similiar tracks!:
            """)
            count = 0

            for i in similar:
                track = i.item
                name = track.get_name()
                artist = track.get_artist()

                similartracks.update({str(count): [name, artist]})
                print(f"[{count}] : {name} by {artist}")

                count += 1

        favs = input(
            """
Which songs would you like to add?
Type their numbers with no spaces: """)
        print(favs)
        favorites = pd.DataFrame(columns=["Title", "Artist"], dtype=str)
        for i in range(len(favs)):

            favorites.loc[len(favorites)] = {
                "Title": similartracks.get(favs[i])[0],
                "Artist": similartracks.get(favs[i])[1].get_name()}

        print("Songs added!")

    elif choice == "2":
        artist = input("Enter an artist name: ")

        inputartist = pylast.Artist(artist, network)
        similar = inputartist.get_similar()

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
                    print(f"{artist}")

    elif choice == "3":
        if favorites.empty:
            print("Add songs to your library!")
        else:
            engine = db.create_engine('sqlite:///favorites.db')
            favorites.to_sql(
                "song",
                con=engine,
                if_exists='append',
                index=False)
            with engine.connect() as connection:
                query_result = connection.execute(
                    db.text("SELECT * FROM song;")).fetchall()
                print(pd.DataFrame(query_result))

    elif choice == "4":
        engine = db.create_engine('sqlite:///favorites.db')
        favorites = pd.DataFrame(columns=["Title", "Artist"])
        favorites.to_sql("song", con=engine, if_exists='replace', index=False)
        exit()


# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works
