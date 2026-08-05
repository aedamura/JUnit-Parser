from analysis.analysis_models import ProjectReport, DependencyGraph, CoverageReport
from documentation.markdown_models import ClassDocumentation, ProjectDocumentation, SummaryDocumentation, \
    MethodDocumentation
from documentation.markdown_writer import MarkdownWriter
from documentation.mermaid_renderer import MermaidRenderer

class MarkdownRenderer:
    # ----------------
    # Index Rendering
    # ----------------

    def render_index(self, project_report: ProjectReport, project_documentation: ProjectDocumentation, dependency_graph: DependencyGraph) -> str:
        writer = MarkdownWriter()

        writer.heading(1, "JUnit Test Documentation")
        writer.heading(2, "Project Summary")

        writer.section(self._render_index_project_summary(project_report))

        writer.horizontal_rule()

        writer.heading(2, "Packages")

        writer.section(self._render_index_packages(project_documentation))

        writer.horizontal_rule()

        writer.heading(2, "Dependency Graph")

        writer.code_block("mermaid", MermaidRenderer().render(dependency_graph, qualified_name=True))


        return writer.build()

    def _render_index_project_summary(self, project_report: ProjectReport) -> str:
        writer = MarkdownWriter()

        writer.bullet(f"Packages: {project_report.metrics.package_count}")
        writer.bullet(f"Test Files: {project_report.metrics.test_file_count}")
        writer.bullet(f"Test Classes: {project_report.metrics.test_class_count}")
        writer.bullet(f"Nested Classes: {project_report.metrics.nested_class_count}")
        writer.bullet(f"Test Methods: {project_report.metrics.test_method_count}")
        writer.bullet(f"Parameterized Tests: {project_report.metrics.parameterized_test_count}")
        writer.bullet(f"Disabled Tests: {project_report.metrics.disabled_test_count}")
        writer.bullet(f"Tagged Tests: {project_report.metrics.tagged_test_count}")
        writer.bullet(f"Lifecycle Methods: {project_report.metrics.lifecycle_method_count}")
        writer.blank_line()

        return writer.build()

    def _render_index_packages(self, project_documentation: ProjectDocumentation) -> str:
        writer = MarkdownWriter()

        for package in project_documentation.packages:
            writer.heading(3, f"`{package}`")

            for cls in project_documentation.classes:
                if cls.package == package:
                    writer.section(self._render_index_class(cls, 0))

        return writer.build()

    def _render_index_class(self, class_documentation: ClassDocumentation, depth: int):
        writer = MarkdownWriter()

        writer.bullet(f"[{class_documentation.class_name}]({class_documentation.root_class}.md#{class_documentation.class_name.lower().replace(" ", "-")})", depth)

        for nested in class_documentation.nested_classes:
            writer.section(self._render_index_class(nested, depth + 1))

        return writer.build()


    # ----------------
    # Coverage Rendering
    # ----------------

    def render_coverage_report(self, coverage_report: CoverageReport) -> str:
        writer = MarkdownWriter()
        writer.heading(1, "Coverage Report")
        writer.paragraph("← [Back to Index](index.md)")

        writer.heading(2, "Coverage")
        for entry in coverage_report.entries:
            writer.heading(3, entry.target)

            for source in entry.tests:
                writer.bullet(f"[{source}]({self._root_class_name(source)}.md#{self._simple_name(source).lower().replace(" ", "-")})")
                writer.blank_line()

        return writer.build()

    # ----------------
    # Test File Rendering
    # ----------------

    def render_class_doc(self, documentation: ClassDocumentation) -> str:
        writer = MarkdownWriter()

        writer.heading(1, documentation.title)
        writer.paragraph(f"**Class:** `{documentation.class_name}`")
        writer.paragraph(f"**Package:** {documentation.package}")
        writer.paragraph("← [Back to Index](index.md)")

        writer.section(self._render_class_body(documentation))

        return writer.build()

    def _render_class_body(self, documentation: ClassDocumentation, depth=0) -> str:
        writer = MarkdownWriter()

        writer.section(self._render_class_summary(documentation.summary, depth+2))

        writer.heading(depth+2, "Dependencies")
        writer.section(self._render_class_dependencies(documentation.dependencies, depth+2))

        writer.heading(depth+2, "Test Methods")
        for method in documentation.methods:
            writer.section(self._render_class_method(method, depth+3))

        for nested in documentation.nested_classes:
            writer.heading(depth+2, f"{nested.title}")
            writer.paragraph(f"**Nested Class:** {nested.class_name}")
            writer.section(self._render_class_body(nested, depth+1))

        return writer.build()

    def _render_class_summary(self, documentation: SummaryDocumentation, depth: int) -> str:
        writer = MarkdownWriter()

        writer.heading(depth, "Summary")

        writer.bullet(f"Tests: {documentation.tests}")
        writer.bullet(f"Disabled: {documentation.disabled}")
        writer.bullet(f"Tagged: {documentation.tagged}")
        writer.blank_line()

        return writer.build()

    def _render_class_dependencies(self, dependencies: DependencyGraph, depth: int) -> str:
        writer = MarkdownWriter()

        if not dependencies.dependencies:
            return writer.build()

        writer.heading(depth+1, "List")

        for dependency in dependencies.dependencies:
            writer.bullet(f"{dependency.target}")
        writer.blank_line()

        writer.heading(depth+1, "Graph")
        writer.code_block("mermaid", MermaidRenderer().render(dependencies))

        return writer.build()

    def _render_class_method(self, method: MethodDocumentation, depth: int) -> str:
        writer = MarkdownWriter()

        writer.heading(depth, f"{method.title}")

        writer.bullet(f"Method Name: `{method.method_name}`")
        writer.bullet(f"Tags: {", ".join(method.tags)}")
        writer.bullet(f"Disabled: {"Yes" if method.disabled else "No"}")
        if method.location:
            writer.bullet(f"Source: {method.location.path}:{method.location.line}")

        writer.blank_line()
        return writer.build()

    # ----------------
    # Helper Functions
    # ----------------

    def _simple_name(self, qualified_name: str) -> str:
        return qualified_name.split(".")[-1]

    def _root_class_name(self, qualified_name: str) -> str:
        for name in qualified_name.split("."):
            if name[0].isupper():
                return name
        return qualified_name.split(".")[-1]