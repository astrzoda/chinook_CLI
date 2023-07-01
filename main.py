from sqlalchemy import MetaData, Table, create_engine, select, func
import argparse
CONNECTION_STRING = "mysql+pymysql://iitis:iitis2023@127.0.0.1:3306/Chinook"


class Foo:
    def __int__(self):
        ...


def start():
    engine = create_engine(CONNECTION_STRING)
    metadata = MetaData()
    metadata.reflect(bind=engine) # the 'reflect' method loads all the tables
    tracks = metadata.tables["Track"]
    artists = metadata.tables["Artist"]
    albums = metadata.tables["Album"]

    parser = argparse.ArgumentParser()

    with engine.connect() as conn:
        # To list all tracks:
        query1 = select(tracks) # python chinook_search.py tracks
        # To list all tracks for given artist:
        query2 = select(artists.c.Name, tracks.c.Name)\
            .join_from(artists, albums)\
            .join_from(albums, tracks)\
            .where(artists.c.Name == "AC/DC")
        # for artist_name, track_name in conn.execute(query2):
        #     print(f"{artist_name}: {track_name}")
        # To list all tracks for given album:
        query3 = select(albums.c.Title, tracks.c.Name)\
            .join_from(albums, tracks)\
            .order_by(albums.c.AlbumId)
        # for album_title, track_name in conn.execute(query3):
        #     print(f"{album_title}: {track_name}")
        # To list all tracks longer than 10000 milliseconds:
        query4 = select(tracks.c.Name, tracks.c.Milliseconds).where(tracks.c.Milliseconds > 10000)
        # for track_name, track_milliseconds in conn.execute(query3):
        #     print(f"{track_name}: {track_milliseconds}")


if __name__ == '__main__':
    start()

