from pathlib import Path

from analysis.dependency_model import DependencyGraph


class DependencyGraphGenerator:

    def generate(self, graph: DependencyGraph, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

        markdown = self._render(graph)

        self._write(output_dir, markdown)


    def _render(self, graph: DependencyGraph) -> str:
        lines = []

        lines.append("# Dependency Graph")
        lines.append("")
        lines.append("This graph shows dependencies from JUnit test classes to imported production classes.")
        lines.append("")
        lines.append("```mermaid")
        lines.append("graph TD")
        lines.append("")

        for dependency in sorted(graph.dependencies, key=lambda d: (d.source, d.target)):
            source = dependency.source.split(".")[-1]
            target = dependency.target.split(".")[-1]

            lines.append(f"{source} --> {target}")

        lines.append("")
        lines.append("```")

        return "\n".join(lines)

    def _write(self, output_dir: Path, markdown: str):
        output_path = output_dir / "dependency_graph.md"

        output_path.write_text(markdown, encoding="utf-8")