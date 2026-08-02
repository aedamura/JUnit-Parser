from pathlib import Path

from analysis.indexer import Indexer
from models import Project
from parsing.parser import JavaParser
from parsing.scanner import FileScanner
from analysis.analyzer import JUnitAnalyzer


class Pipeline:

    def __init__(self, scanner: FileScanner, parser: JavaParser, analyzer: JUnitAnalyzer, indexer: Indexer):
        self._scanner = scanner
        self._parser = parser
        self._analyzer = analyzer
        self._indexer = indexer

    def run(self, input_directory: Path) -> Project:
        project = self._scanner.scan(input_directory)


        for test_file in project.test_files:
           self._parser.parse(test_file)

        self._analyzer.analyze(project)

        project = self._indexer.index(project)

        return project