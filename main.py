from pathlib import Path

from application import Application
from analysis.dependency_analyzer import DependencyAnalyzer
from analysis.analyzer import JUnitAnalyzer
from documentation.dependency_generator import DependencyGraphGenerator
from analysis.indexer import Indexer
from documentation.markdown_generator import MarkdownGenerator
from parsing.parser import JavaParser
from pipline import Pipeline
from parsing.scanner import FileScanner


def main():
    application = Application(
        Pipeline(
            FileScanner(),
            JavaParser(),
            JUnitAnalyzer(),
            Indexer()
        ),
        MarkdownGenerator(),
        DependencyAnalyzer(),
        DependencyGraphGenerator()
    )

    application.run(
        Path("tests"),
        Path("docs")
    )

if __name__ == "__main__":
    main()