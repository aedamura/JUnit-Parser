import argparse
from pathlib import Path

from analysis.coverage_analyzer import CoverageAnalyzer
from analysis.project_analyzer import ProjectAnalyzer
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
    parser = argparse.ArgumentParser(description="Generate Markdown documentation for JUnit test suites.")
    parser.add_argument("source", type=str, help="Path to the source directory containing Java test files.")
    parser.add_argument("output", type=str, help="Path to the output directory where documentation will be generated.", default="docs")
    args = parser.parse_args()
    
    application = Application(
        Pipeline(
            FileScanner(),
            JavaParser(),
            JUnitAnalyzer(),
            Indexer()
        ),
        MarkdownGenerator(),
        ProjectAnalyzer(),
        DependencyAnalyzer(),
        CoverageAnalyzer(),
        DependencyGraphGenerator()
    )

    num_test_files = application.run(
        Path(args.source),
        Path(args.output)
    )

    print(f"Generated documentation for {num_test_files} test files.")
    print(f"Source directory: {args.source}")
    print(f"Output directory: {args.output}")



if __name__ == "__main__":
    main()