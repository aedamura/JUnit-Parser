from pathlib import Path

from dependency_analyzer import DependencyAnalyzer
from dependency_generator import DependencyGraphGenerator
from markdown_generator import MarkdownGenerator
from pipline import Pipeline


class Application:
    def __init__(
        self,
        pipeline: Pipeline,
        markdown_generator: MarkdownGenerator,
        dependency_analyzer: DependencyAnalyzer,
        dependency_graph_generator: DependencyGraphGenerator
    ):
        self._pipeline = pipeline
        self._markdown_generator = markdown_generator
        self._dependency_analyzer = dependency_analyzer
        self._dependency_graph_generator = dependency_graph_generator


    def run(self, input_directory: Path, output_directory: Path,):
        project = self._pipeline.run(input_directory)

        dependency_graph = self._dependency_analyzer.analyze(project)

        self._markdown_generator.generate(project, dependency_graph, output_directory)

        self._dependency_graph_generator.generate(dependency_graph, output_directory)


    