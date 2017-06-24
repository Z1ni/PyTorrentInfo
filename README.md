PyTorrentInfo
=============

Parse bencoded data (torrent files, tracker responses) using Python 3

How to use
----------

With torrent file:
```python
import torrentParser

tp = torrentParser.TorrentParser()
data = tp.readFile("/file/path/here")
torrentName = data["torrent"]["info"]["name"]
```

With tracker response (string with bencoded data):
```python
import torrentParser

tp = torrentParser.TorrentParser()
data = tp.readDict("d3:bar4:spam3:fooi42ee")
```

You can also use bundled torrentInfo.py as a command line program.
Parameters:

Parameter | What?
----------|------
-d / --dump | Dumps the file as parsed dictionary (with hashes!)
-D / --dump-without-hashes | Dumps the file as parsed dictionary, but without the hashes
-k / --key | Returns only the specified key-value pair

Hashes make the output harder to read, so don't print them if you don't really need to see them


Test Data
---------
The test data in this repo is a random selection of .torrent files from archive.org. I have not downloaded or assessed the content itself.
