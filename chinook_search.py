from sqlalchemy import MetaData, Table, create_engine, select, func
import argparse
CONNECTION_STRING = "mysql+pymysql://iitis:iitis2023@127.0.0.1:3306/Chinook"


class Foo:
    def __int__(self):
        ...


def start(args):
    engine = create_engine(CONNECTION_STRING)
    metadata = MetaData()
    metadata.reflect(bind=engine) # the 'reflect' method loads all the tables
    tracks = metadata.tables["Track"]
    artists = metadata.tables["Artist"]
    albums = metadata.tables["Album"]
    # all conditions
    # SELECT Artist.Name AS ArtistName, Album.Title, Track.Name as TrackName, Track.Milliseconds
    # FROM Artist RIGHT JOIN Album ON Artist.ArtistId = Album.AlbumId
    # JOIN Track ON Track.TrackId = Album.AlbumId
    # HAVING Artist.Name = "AC/DC" AND Track.Milliseconds >= 10000000
    # ORDER BY Track.Milliseconds
    # LIMIT 5
    if args.artist and args.album and args.ms and args.ms and args.limit and args.order_by:
        # threshold = [float(s) for s in args.ms.split() if s.isdigit()][0]
        # print(threshold)
        # if args.ms[0] == ">":
        #     if args.ms[1] == "=":
        #         foo = func(tracks.c.Milliseconds >= args.ms)
        #     else:
        #         foo = func(tracks.c.Milliseconds > args.ms)
        # elif args.ms[0] == "=":
        #     foo = func(tracks.c.Milliseconds == args.ms)
        # else:
        #     pass
        query = select(artists.c.Name, albums.c.Title, tracks.c.Name, tracks.c.Milliseconds)\
            .join_from(artists, albums)\
            .join_from(tracks, albums)\
            .having((artists.c.Name == args.artist) & (tracks.c.Milliseconds > 2))\
            .limit(args.limit)\
            .order_by(args.order_by)

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

def foo():
    print("artist is provided")
    # all conditions
    # SELECT Artist.Name AS ArtistName, Album.Title, Track.Name as TrackName, Track.Milliseconds
    # FROM Artist RIGHT JOIN Album ON Artist.ArtistId = Album.AlbumId
    # JOIN Track ON Track.TrackId = Album.AlbumId
    # HAVING Artist.Name = "AC/DC" AND Track.Milliseconds BETWEEN 100 AND 10000000
    # ORDER BY Track.Milliseconds
    # LIMIT 5


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist', type=str)
    parser.add_argument('--album', type=str)
    parser.add_argument("--ms", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--order_by", type=str)
    arguments = parser.parse_args()
    start(arguments)




