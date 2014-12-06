PyTorrentInfo
=============

Parse bencoded data (torrent files, tracker responses) using Python 3

How to use
----------

With torrent file:
```python
import torrentParser

data = torrentParser.readFile("/file/path/here")
torrentName = data["torrent"]["info"]["name"]
```

With tracker response (string with bencoded data):
```python
import torrentParser
from io import BytesIO

text_data = BytesIO("d3:bar4:spam3:fooi42ee".encode("utf-8"))

data = torrentParser.readDict(text_data, 0, True)
```

You can also use bundled torrentInfo.py as a command line program.
Parameters:

Parameter | What?
----------|------
-d / --dump | Dumps the file as parsed dictionary (with hashes!)
-D / --dump-without-hashes | Dumps the file as parsed dictionary, but without the hashes
-k / --key | Returns only the specified key-value pair

Hashes make the output harder to read, so don't print them if you don't really need to see them
