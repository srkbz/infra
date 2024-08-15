#!/usr/bin/env python3
from sys import argv
from os import makedirs
from os.path import join, dirname
import xml.etree.ElementTree as ET


class SecretsXMLWalker:
    _tree: ET.ElementTree
    _files: dict[str, dict[str, str]]

    def __init__(self, xml_path) -> None:
        self._tree = ET.parse(xml_path)
        self._files = {}

    def walk(self):
        doc = self._tree.getroot()

        for item in doc:
            if item.tag == "Root":
                root = item

                for item in root:
                    if item.tag == "Group":
                        self.walk_group(item, [], root=True)

    def dump(self):
        for file, content in self._files.items():
            makedirs(dirname(file), exist_ok=True)
            with open(file, "w") as f:
                for key, value in content.items():
                    f.write(f"{key}={value}\n")

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

                    file = join(*breadcrumb, entry_title + ".env")
                    if file not in self._files:
                        self._files[file] = {}
                    self._files[file][key.upper()] = value


walker = SecretsXMLWalker(argv[1])
walker.walk()
walker.dump()
