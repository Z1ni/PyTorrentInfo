PyTorrentInfo
=============

Parse bencoded torrent files using Python 3

How to use
----------

```python
import torrentParser

data = torrentParser.readFile("/file/path/here")
torrentName = data["torrent"]["info"]["name"]
...
```

You can also use torrentInfo.py as a command line program.
Parameters:

Parameter | What?
----------|------
-d / --dump | Dumps the file as parsed dictionary (with hashes!)
-D / --dump-without-hashes | Dumps the file as parsed dictionary, but without the hashes

Hashes make the output harder to read, so don't print them if you don't really need to see them
