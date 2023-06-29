import sqlalchemy as db
import pandas as pd


def view_library(favorites):
    # If user didn't favorite any songs will return a message
    if favorites.empty:
        print("Add songs to your library!")
    else:
        # Returns favorited songs using an SQL query
        engine = db.create_engine('sqlite:///favorites.db')
        favorites.to_sql(
            "song",
            con=engine,
            if_exists='append',
            index=False)
        with engine.connect() as connection:
            query_result = connection.execute(
                db.text("SELECT DISTINCT * FROM song;")).fetchall()
            return pd.DataFrame(query_result)
