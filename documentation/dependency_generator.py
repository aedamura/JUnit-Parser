from pathlib import Path

from analysis.analysis_models import DependencyGraph
from documentation.markdown_writer import MarkdownWriter
from documentation.mermaid_renderer import MermaidRenderer


class DependencyGraphGenerator:

    def generate(self, graph: DependencyGraph, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

        markdown = self._render(graph)

        self._write(output_dir, markdown)


    def _render(self, graph: DependencyGraph) -> str:
        writer = MarkdownWriter()

        writer.heading(1, "Dependency Graph")
        writer.line("This graph shows dependencies from JUnit test classes to imported production classes.")
        writer.blank_line()

        renderer = MermaidRenderer()

        text = ""
        for dependency in sorted(graph.dependencies, key=lambda d: (d.source, d.target)):
            text += renderer.render(graph, dependency.source) + "\n"

        writer.code_block("mermaid", text)

        return writer.build()

    def _write(self, output_dir: Path, markdown: str):
        output_path = output_dir / "dependency_graph.md"

        output_path.write_text(markdown, encoding="utf-8")