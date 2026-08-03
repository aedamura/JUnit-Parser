from pathlib import Path
from version import __version__
from datetime import datetime

from models import Project, TestClass, TestFile, TestMethod
from documentation.markdown_models import ClassDocumentation, MethodDocumentation, SummaryDocumentation
from documentation.markdown_writer import MarkdownWriter
from documentation.mermaid_renderer import MermaidRenderer
from analysis.analysis_models import DependencyGraph, ProjectReport, CoverageReport


class MarkdownGenerator:

    def generate(self, project: Project, dependency_graph: DependencyGraph, project_report: ProjectReport, coverage_report: CoverageReport, output_dir: Path) -> None:

        output_dir.mkdir(parents=True, exist_ok=True)

        for test_file in project.test_files:
            for test_class in test_file.classes:

                documentation = self._create_class_documentation(
                    test_file,
                    test_class,
                    dependency_graph
                )

                self._write_class_doc(
                    output_dir,
                    documentation,
                )

        self._write_index(project, project_report, dependency_graph, output_dir)
        self._write_coverage_report(project, coverage_report, output_dir)

    # ------------
    # Documentation Object Constructors
    # ------------

    def _create_class_documentation(self, test_file: TestFile, test_class: TestClass, dependency_graph: DependencyGraph) -> ClassDocumentation:
        methods, summary = self._collect_methods(test_class)

        nested = [
            self._create_class_documentation(
                test_file,
                nested_class,
                dependency_graph
            ) for nested_class in test_class.nested_classes
        ]

        return ClassDocumentation(
            title=self._get_title(test_class),
            class_name=test_class.name,
            package=self._get_package(test_file),
            dependencies=DependencyGraph(dependency_graph.dependencies_for(test_class.qualified_name)),
            summary=summary,
            methods=methods,
            nested_classes=nested
        )

    def _create_method_documentation(self, method: TestMethod) -> MethodDocumentation:
        return MethodDocumentation(
            title=method.display_name or method.name,
            method_name=method.name,
            tags=method.tags,
            disabled=method.is_disabled,
            location=method.location
        )

    # ------------
    # Rendering Functions
    # ------------

    def _render(self, documentation: ClassDocumentation) -> str:
        writer = MarkdownWriter()

        writer.section(self._render_class_title(documentation))
        writer.section(self._render_package(documentation.package))

        writer.section(self._render_class_body(documentation, 2))

        return writer.build()

    def _render_class_title(self, documentation: ClassDocumentation, level: int = 1) -> str:
        writer = MarkdownWriter()

        writer.heading(level, documentation.title)
        writer.line(f"**Class:** `{documentation.class_name}`")
        writer.blank_line()

        return writer.build()

    def _render_package(self, package: str) -> str:
        writer = MarkdownWriter()

        writer.heading(2, "Package")
        writer.line(package)
        writer.blank_line()

        return writer.build()

    def _render_summary(self, summary: SummaryDocumentation, level:int = 2) -> str:
        writer = MarkdownWriter()

        writer.heading(level, "Summary")
        writer.bullet(f"Tests: {summary.tests}")
        writer.bullet(f"Disabled: {summary.disabled}")
        writer.bullet(f"Tagged: {summary.tagged}")
        writer.blank_line()

        return writer.build()

    def _render_methods(self, methods: list[MethodDocumentation], level: int = 2) -> str:
        writer = MarkdownWriter()

        writer.heading(level, "Test Methods")

        for method in methods:
            writer.heading(level+1, method.title)
            writer.bullet(f"Method: `{method.method_name or method.title}`")
            writer.bullet(f"Tags: {", ".join(method.tags)}")
            writer.bullet(f"Disabled: {"Yes" if method.disabled else "No"}")
            writer.bullet(f"Source: {
                "Unknown" if method.location is None 
                else method.location.path + ":" + str(method.location.line)}"
            )
            writer.blank_line()

        return writer.build()

    def _render_dependencies(self, dependency_graph: DependencyGraph, level: int = 2) -> str:
        writer = MarkdownWriter()

        writer.heading(level, "Dependencies")

        if len(dependency_graph.dependencies) == 0:
            return writer.build()

        writer.heading(level+1, "List")
        for dependency in dependency_graph.dependencies:
            writer.bullet(dependency.target)
        writer.blank_line()

        writer.heading(level+1, "Graph")
        writer.code_block("mermaid", MermaidRenderer().render(dependency_graph))

        return writer.build()

    def _render_class_body(self, documentation: ClassDocumentation, level: int) -> str:
        writer = MarkdownWriter()

        writer.section(self._render_summary(documentation.summary, level))
        writer.section(self._render_dependencies(documentation.dependencies, level))
        writer.section(self._render_methods(documentation.methods, level))

        for nested in documentation.nested_classes:

            writer.section(self._render_class_title(nested, level))
            writer.section(self._render_class_body(nested, level+1))

        return writer.build()

    # ----------
    # File Writing Functions
    # ----------

    def _write_class_doc(self, output_dir: Path, documentation: ClassDocumentation):
        writer = MarkdownWriter()

        writer.section(self._render_class_title(documentation))
        writer.section(self._render_package(documentation.package))

        writer.section(self._render_class_body(documentation, 2))

        self._write_file(output_dir, f"{documentation.class_name}.md", writer)

    def _write_index(self, project: Project, project_report: ProjectReport, dependency_graph: DependencyGraph, output_dir: Path):
        writer = MarkdownWriter()

        writer.heading(1, "JUnit Test Documentation")

        writer.heading(2, "Project Summary")

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

        writer.horizontal_rule()

        writer.heading(2, "Packages")

        packages = self._collect_packages_and_classes(project.test_files)

        for package in packages:
            writer.heading(3, package)

            for entry in packages[package]:
                writer.bullet(f"[{entry[0]}]({entry[1]})", entry[2])
            writer.blank_line()

        writer.horizontal_rule()

        writer.heading(2, "Dependency Graph")

        writer.code_block("mermaid", MermaidRenderer().render(dependency_graph, qualified_name=True))

        self._write_file(output_dir, "index.md", writer)

    def _write_coverage_report(self, project: Project, coverage_report: CoverageReport, output_dir: Path):
        writer = MarkdownWriter()

        writer.heading(1, "Coverage Report")

        writer.heading(2, "Coverage")
        for entry in coverage_report.entries:
            writer.heading(3, entry.target)

            for source in entry.tests:
                writer.bullet(f"[{source}]({source}.md)")
            writer.blank_line()

        self._write_file(output_dir, "coverage_report.md", writer)

    def _write_file(self, output_dir: Path, filename: str, writer: MarkdownWriter):
        writer.horizontal_rule()
        writer.line(f"Generated by JUnit Structure Parser v{__version__}")
        writer.line(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        output_path = output_dir / filename
        output_path.write_text(writer.build(), encoding="utf-8")

    # ------------
    # Data Collection Functions
    # ------------

    def _collect_packages_and_classes(self, files: list[TestFile]) -> dict[str, list[tuple[str, str, int]]]:
        packages = {}

        for file in files:
            package = file.package
            package_entries = []

            packages.setdefault(package, package_entries)

            file_class = file.classes[0]

            for cls in file.classes:
                self._collect_package_classes(cls, package_entries, document_name=file_class.name+".md", depth=0)

        return packages

    def _collect_package_classes(self, test_class: TestClass, entries: list[tuple[str,str,int]],document_name: str, depth: int):
        entries.append(
            (test_class.name, document_name, depth)
        )

        for nested in test_class.nested_classes:
            self._collect_package_classes(nested, entries, document_name, depth+1)

    def _collect_methods(self, test_class: TestClass) -> tuple[list[MethodDocumentation], SummaryDocumentation]:

        methods = []

        summary = SummaryDocumentation()

        for method in test_class.methods:

            if method.is_test:
                summary.tests+=1

                if method.is_disabled:
                    summary.disabled+=1

                if method.tags:
                    summary.tagged+=1

                methods.append(self._create_method_documentation(method))

        return methods, summary

    # -----------------
    # Project Summary Functions
    # -----------------

    def _count_packages(self, project: Project) -> int:
        return len({
            test_file.package
            for test_file in project.test_files
            if test_file.package != "(default)"
        })

    def _count_classes_from_files(self, files: list[TestFile]) -> int:
        total = 0

        for file in files:
            total += self._count_classes(file.classes)

        return total

    def _count_classes(self, classes: list[TestClass]) -> int:
        total = 0

        for cls in classes:

            total += 1

            total += self._count_classes(cls.nested_classes)

        return total

    def _count_test_methods_from_files(self, files: list[TestFile]) -> int:
        total = 0

        for file in files:

            total += self._count_test_methods(file.classes)

        return total

    def _count_test_methods(self, classes: list[TestClass]) -> int:
        total = 0

        for cls in classes:
            total += sum(
                1
                for method in cls.methods
                if method.is_test
            )

            total += self._count_test_methods(cls.nested_classes)

        return total

    def _count_disabled_methods_from_files(self, files: list[TestFile]) -> int:
            total = 0
    
            for file in files:
    
                total += self._count_disabled_methods(file.classes)
    
            return total

    def _count_disabled_methods(self, classes: list[TestClass]) -> int:

        total = 0

        for cls in classes:
            total += sum(
                1
                for method in cls.methods
                if method.is_test
                and method.is_disabled
            )

            total += self._count_disabled_methods(cls.nested_classes)

        return total

    # --------------
    # Helper Functions
    # --------------

    def _get_package(self, test_file: TestFile) -> str:
        return test_file.package

    def _get_title(self, test_class: TestClass) -> str:
        return test_class.display_name or test_class.name

    def _get_class_name(self, test_class: TestClass) -> str:
        return test_class.name
