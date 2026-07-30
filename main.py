from pathlib import Path

from application import Application
from dependency_analyzer import DependencyAnalyzer
from dependency_generator import DependencyGraphGenerator
from indexer import Indexer
from markdown_generator import MarkdownGenerator
from parser import JavaParser
from pipline import Pipeline
from scanner import FileScanner


def main():
    application = Application(
        Pipeline(
            FileScanner(),
            JavaParser(),
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