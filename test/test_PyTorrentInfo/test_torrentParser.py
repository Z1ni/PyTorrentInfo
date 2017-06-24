#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import io
import os
import unittest

from PyTorrentInfo.torrentParser import TorrentParser

class TestTorrentParser(unittest.TestCase):

    def setUp(self):
        self.tp = TorrentParser()

    def test_positive_and_negative_integers(self):
        self.tp.file = io.BytesIO(b"i1900e")
        self.assertEqual(1900, self.tp.readInt())

        self.tp.file = io.BytesIO(b"i-10e")
        self.assertEqual(-10, self.tp.readInt())

