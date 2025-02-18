#!/usr/bin/env python3
from sys import argv
import xml.etree.ElementTree as ET
import json


class SecretsXMLWalker:
    _tree: ET.ElementTree
    _db: dict[str, dict[str, str]]

    def __init__(self, xml_path) -> None:
        self._tree = ET.parse(xml_path)
        self._db = {}

    def walk(self):
        doc = self._tree.getroot()

        for item in doc:
            if item.tag == "Root":
                root = item

                for item in root:
                    if item.tag == "Group":
                        self.walk_group(item, [], root=True)

    def dump(self):
        with open(argv[2], "w") as f:
            json.dump(self._db, f, indent=2)

    def walk_group(self, group: ET.Element, breadcrumb: list[str], root=False):
        group_name = group.find("./Name").text
        breadcrumb = [*breadcrumb, group_name] if not root else [*breadcrumb]
        for item in group:
            if item.tag == "Group":
                self.walk_group(item, breadcrumb)
                continue

            if item.tag == "Entry":
                self.walk_entry(item, breadcrumb)
                continue

    def walk_entry(self, entry: ET.Element, breadcrumb: list[str]):
        entry_title = entry.find('./String/[Key="Title"]/Value').text
        for item in entry:
            if item.tag == "String":
                key = item.find("./Key").text
                value = item.find("./Value").text
                if key != "Title" and value is not None:

                    entry = "/".join([*breadcrumb, entry_title])
                    if entry not in self._db:
                        self._db[entry] = {}
                    self._db[entry][key.upper()] = value


walker = SecretsXMLWalker(argv[1])
walker.walk()
walker.dump()
