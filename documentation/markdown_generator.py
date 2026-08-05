from pathlib import Path

from models import Project
from documentation.markdown_models import ProjectDocumentation
from documentation.markdown_renderer import MarkdownRenderer
from documentation.markdown_writer import MarkdownWriter
from analysis.analysis_models import DependencyGraph, ProjectReport, CoverageReport


class MarkdownGenerator:

    def generate(
            self,
            project: Project,
            dependency_graph: DependencyGraph,
            project_report: ProjectReport,
            project_documentation: ProjectDocumentation,
            coverage_report: CoverageReport,
            output_dir: Path
    ):

        output_dir.mkdir(parents=True, exist_ok=True)

        self._generate_index(project_report,project_documentation, dependency_graph, output_dir)
        self._generate_class_docs(project_documentation, dependency_graph, output_dir)
        self._generate_coverage_report(coverage_report, output_dir)

    # ----------
    # File Writing Functions
    # ----------

    def _generate_class_docs(self, project_documentation: ProjectDocumentation, dependency_graph: DependencyGraph, output_dir: Path):
        writer = MarkdownWriter()

        for cls in project_documentation.classes:
            writer.section(MarkdownRenderer().render_class_doc(cls))

            writer.write_to_file(f"{cls.class_name}.md", output_dir)
            writer.clear()

    def _generate_index(
            self,
            project_report: ProjectReport,
            project_documentation: ProjectDocumentation,
            dependency_graph: DependencyGraph,
            output_dir: Path
    ):
        writer = MarkdownWriter()

        writer.section(MarkdownRenderer().render_index(project_report, project_documentation, dependency_graph))

        writer.write_to_file("index.md", output_dir)

    def _generate_coverage_report(self, coverage_report: CoverageReport, output_dir: Path):
        writer = MarkdownWriter()

        writer.section(MarkdownRenderer().render_coverage_report(coverage_report))

        writer.write_to_file("coverage_report.md", output_dir)
