from pathlib import Path

from indexer import Indexer
from models import Project
from parser import JavaParser
from scanner import FileScanner


class Pipeline:

    def __init__(self, scanner: FileScanner, parser: JavaParser, indexer: Indexer):
        self._scanner = scanner
        self._parser = parser
        self._indexer = indexer

    def run(self, input_directory: Path) -> Project:
        project = self._scanner.scan(input_directory)


        for test_file in project.test_files:
           self._parser.parse(test_file)

        project = self._indexer.index(project)

        return project