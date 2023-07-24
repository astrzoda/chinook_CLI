from argparse import ArgumentParser
from typing import Callable
import re
from sqlalchemy import create_engine, MetaData, select, func

CONNECTION_STRING = "mysql+pymysql://iitis:iitis2023@127.0.0.1:3306/Chinook"


def make_query(args):
    engine = create_engine(CONNECTION_STRING)
    metadata = MetaData()
    metadata.reflect(bind=engine)  # the 'reflect' method loads all the tables
    artists, tracks, albums = (
        metadata.tables["Artist"],
        metadata.tables["Track"],
        metadata.tables["Album"],
    )

    with engine.connect() as conn:
        # To list all tracks:
        query = (
            select(
                tracks.c.Name.label("track"),
                artists.c.Name.label("artist"),
                albums.c.Title.label("album_title"),
                tracks.c.Milliseconds.label("milliseconds"),
            )
            .join_from(artists, albums)
            .join_from(albums, tracks)
        )  # To list all tracks:
        # query = select(tracks)
        if args.artist:
            # To list all albums for given artist:
            query = query.where(artists.c.Name == args.artist)
        if args.limit:
            query = query.limit(args.limit)
        if args.order_by:
            query = query.order_by(args.order_by)
        if args.ms:
            sign, number = extract_components(arg=args.ms)
            query = complete_query_with_millisecond_limit(
                sign, number, query, interesting_column=tracks.c.Milliseconds
            )
        display_query_result(connection=conn, query=query)

def display_query_result(connection, query):
    for track_name, artist_name, album_title, track_milliseconds in connection.execute(
        query
    ):
        print(
            f"track: {track_name}, artist: {artist_name}, album_title: {album_title}, "
            f"milliseconds: {track_milliseconds}"
        )


def complete_query_with_millisecond_limit(sign, number, query, interesting_column):
    if sign == ">":
        query = query.having(interesting_column > number)
    elif sign == ">=":
        query = query.having(interesting_column >= number)
    elif sign == "<":
        query = query.having(interesting_column < number)
    elif sign == "<=":
        query = query.having(interesting_column <= number)
    elif sign == "=":
        query = query.having(interesting_column == number)
    else:
        raise ValueError("Incorrect sign")
    return query


def extract_components(arg):
    number = float(re.findall("[0-9]+", arg)[0])
    pattern = r"[><]=?|a="
    sign = re.findall(pattern, arg)[0]
    return sign, number


def handle_tracks(args):
    print("Searching for tracks!")
    make_query(args)


def handle_albums(args):
    print("Searching for albums!")
    if args.artist:
        print("artist is not None")


def main():
    parser = ArgumentParser(description="Program to search Chinook")
    # Add arguments
    subparsers = parser.add_subparsers(required=True)

    base_parser = ArgumentParser(add_help=False)
    base_parser.add_argument("--artist", type=str)
    base_parser.add_argument("--limit", type=int)
    base_parser.add_argument("--ms", type=str)
    base_parser.add_argument("--order_by", type=str, choices=["milliseconds", "track", "artist", "album_title"]) # to improve
    base_parser.add_argument(
        "--verbose", help="Turns verbose output", action="store_true"
    )
    tracks_parser = subparsers.add_parser("tracks", parents=[base_parser])
    tracks_parser.add_argument(
        "--album", type=str, help="Album for which tracks should be found"
    )
    tracks_parser.set_defaults(command=handle_tracks)
    albums_parser = subparsers.add_parser("albums", parents=[base_parser])
    albums_parser.set_defaults(command=handle_albums)

    args = parser.parse_args()

    if args.verbose:
        print("Yay! In verbose mode!")

    args.command(args)


if __name__ == "__main__":
    main()
