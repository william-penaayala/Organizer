#!/usr/bin/env python3

from ImageSpells import *

class MagicTagset:
    def __init__(self):
        self.tags = {}
        default_tag = MagicTag("default")
        self.tags[default_tag.name] = default_tag

    def add(self, tag):
        if tag.name not in self.tags.keys():
            self.tags[tag.name] = tag
            return True
        else:
            return False

    def get(self, tag_name):
        if tag_name in self.tags.keys():
            return self.tags[tag_name]
        else:
            return self.tags["default"]
