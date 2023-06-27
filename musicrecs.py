import pylast

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

# Now you can use that object everywhere
track = network.get_track("beabadoobee", "Apple Cider")
track.love()
track.add_tags(("awesome", "favorite"))

print(track)

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works