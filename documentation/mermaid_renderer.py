from analysis.analysis_models import DependencyGraph
from documentation.markdown_writer import MarkdownWriter

class MermaidRenderer:

    def render(
        self,
        graph: DependencyGraph,
        qualified_name: bool = False
    ) -> str:
        writer = MarkdownWriter()
        writer.line("graph TD")

        for dependency in sorted(graph.dependencies, key=lambda d: d.source):
            if qualified_name:
                writer.line(f"{dependency.source} --> {dependency.target}")
            else:
                writer.line(f"{self._simple_name(dependency.source)} --> {self._simple_name(dependency.target)}")

        return writer.build()

    def _simple_name(self, qualified_name: str) -> str:
        return qualified_name.split(".")[-1]