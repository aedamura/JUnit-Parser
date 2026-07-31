from dependency_model import DependencyGraph
from markdown_writer import MarkdownWriter
from models import TestClass


class MermaidRenderer:

    def render(
        self,
        graph: DependencyGraph,
        source: str
    ) -> str:
        writer = MarkdownWriter()
        writer.line("graph TD")
        writer.blank_line()

        for dependency in graph.dependencies_for(source):
            writer.line(f"{self._simple_name(source)} --> {self._simple_name(dependency.target)}")

        return writer.build()


    def _simple_name(
        self,
        qualified_name: str
    ) -> str:
        return qualified_name.split(".")[-1]