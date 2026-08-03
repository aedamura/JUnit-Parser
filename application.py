from pathlib import Path

from analysis.coverage_analyzer import CoverageAnalyzer
from analysis.dependency_analyzer import DependencyAnalyzer
from analysis.project_analyzer import ProjectAnalyzer
from documentation.dependency_generator import DependencyGraphGenerator
from documentation.markdown_generator import MarkdownGenerator
from pipline import Pipeline


class Application:
    def __init__(
        self,
        pipeline: Pipeline,
        markdown_generator: MarkdownGenerator,
        project_analyzer: ProjectAnalyzer,
        dependency_analyzer: DependencyAnalyzer,
        coverage_analyzer: CoverageAnalyzer,
        dependency_graph_generator: DependencyGraphGenerator
    ):
        self._pipeline = pipeline
        self._markdown_generator = markdown_generator
        self._project_analyzer = project_analyzer
        self._dependency_analyzer = dependency_analyzer
        self._coverage_analyzer = coverage_analyzer
        self._dependency_graph_generator = dependency_graph_generator


    def run(self, input_directory: Path, output_directory: Path,) -> int:
        project = self._pipeline.run(input_directory)

        project_report = self._project_analyzer.analyze(project)

        dependency_graph = self._dependency_analyzer.analyze(project)

        coverage_report = self._coverage_analyzer.analyze(dependency_graph)

        self._markdown_generator.generate(project, dependency_graph, project_report, coverage_report,output_directory)

        self._dependency_graph_generator.generate(dependency_graph, output_directory)

        return len(project.test_files)


    