#!/usr/bin/python3

import torrentParser as TP
import argparse
from datetime import datetime as dt


argParser = argparse.ArgumentParser(description="View/dump torrent file info")
argParser.add_argument("-d", "--dump", dest="full_dump", action="store_true", help="Dump parsed data with piece hashes")
argParser.add_argument("-D", "--dump-without-hashes", dest="dump", action="store_true", help="Dump parsed data without piece hashes")
argParser.add_argument("file", help="torrent file")

args = argParser.parse_args()


path = args.file

parsed = TP.readFile(path)

torrent = parsed["torrent"]
info = torrent["info"]

private = False

try:
    if info["private"] == 1:
        private = True
except:
    private = False

if not args.dump and not args.full_dump:

    # This data is mandatory
    print("Torrent name: %s" % info["name"])
    print("Contains %i file(s) and %i pieces" % (len(info["files"]), len(info["pieces"])))
    if not private:
        print("Announce URL: %s" % torrent["announce"])
        print("This is not a private torrent")
    else:
        print("This is a private torrent")

    # These are optional, AFAIK
    try:
        print("Created by: %s" % torrent["created by"])
        print("Creation date: %s" % dt.fromtimestamp(torrent["creation date"]).strftime("%d.%m.%Y %H:%M:%S"))
        print("Encoding: %s" % torrent["encoding"])
    except:
        pass

elif args.dump:
    # Dump excluding hashes
    parsed["torrent"]["info"].pop("pieces", None)
    print(parsed)

elif args.full_dump:
    # Dump with hashes
    print(parsed)
