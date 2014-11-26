#!/usr/bin/python3

import torrentParser as TP
import argparse
from datetime import datetime as dt


def finditem(obj, key):
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = finditem(v, key)
            if item is not None:
                return item


argParser = argparse.ArgumentParser(description="View/dump torrent file info")
argParser.add_argument("-d", "--dump", dest="full_dump", action="store_true", help="Dump parsed data with piece hashes")
argParser.add_argument("-D", "--dump-without-hashes", dest="dump", action="store_true", help="Dump parsed data without piece hashes")
argParser.add_argument("-k", "--key", metavar="K", dest="key", help="Key to be displayed")
argParser.add_argument("file", help="torrent file")

args = argParser.parse_args()


path = args.file

parsed = TP.readFile(path)

torrent = parsed["torrent"]
info = torrent["info"]

private = False
trackerless = False

try:
    if info["private"] == 1:
        private = True
except:
    # If private key is not found this is not a private torrent
    private = False

# If torrent file doesn't contain announce or announce-list keys, it's a trackerless torrent
if torrent.get("announce") is None and torrent.get("announce-list") is None:
    trackerless = True
    # Trackerless torrents have node list
    nodes = torrent["nodes"]
else:
    if torrent.get("announce") is not None:
        trackers = [torrent["announce"]]
    else:
        trackers = torrent["announce-list"]

if not args.dump and not args.full_dump and args.key is None:

    print("Torrent name: %s" % info["name"])
    # pieces is a hash list containing piece hashes. SHA-1 hash is 20 bytes long.
    # Every piece has a hash so the piece count is info["pieces"] / 20
    try:
        print("Contains %i file(s) and %i pieces" % (len(info["files"]), int(len(info["pieces"]) / 20)))
    except:
        # It seems that files and pieces are not mandatory because httpseeds key
        pass
    if not private:
        if not trackerless:
            print("Announce URL(s): %s" % ", ".join(trackers))
        else:
            print("This is a trackerless torrent.")
            print("Nodes:")
            print("\t" + nodes)
        print("This is not a private torrent")
    else:
        print("This is a private torrent")

    if torrent.get("httpseeds") is not None:
        print("HTTP seeds: %s" % ", ".join(torrent["httpseeds"]))

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

elif args.key is not None:
    # Dump only one key
    print(finditem(parsed, args.key))

exit()
