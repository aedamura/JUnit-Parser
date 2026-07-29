from pathlib import Path

from models import Project, TestClass, TestFile, TestMethod
from markdown_models import ClassDocumentation, MethodDocumentation, SummaryDocumentation


class MarkdownGenerator:

    def generate(self, project: Project, output_dir: Path) -> None:

        output_dir.mkdir(parents=True, exist_ok=True)

        for test_file in project.test_files:
            for test_class in test_file.classes:

                documentation = self._create_documentation(
                    test_file,
                    test_class
                )

                markdown = self._render(documentation)

                self._write(
                    output_dir,
                    test_class,
                    markdown
                )

    def _create_documentation(self, test_file: TestFile, test_class: TestClass) -> ClassDocumentation:
        methods, summary = self._collect_methods(test_class)

        return ClassDocumentation(
            title=self._get_title(test_class),
            class_name=test_class.name,
            package=self._get_package(test_file),
            summary=summary,
            methods=methods
        )

    def _render(self, documentation: ClassDocumentation) -> str:
        lines = []

        lines.extend(self._render_title(documentation.title, documentation.class_name))
        lines.extend(self._render_package(documentation.package))
        lines.extend(self._render_summary(documentation.summary))
        lines.extend(self._render_methods(documentation.methods))

        return "\n".join(lines)

    def _write(self, output_dir: Path, test_class: TestClass, markdown: str):
        output_path = output_dir / (
            test_class.name + ".md"
        )

        output_path.write_text(markdown, encoding="utf-8")

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

                methods.append(self._create_method(method))

        return methods, summary

    def _create_method(self, method: TestMethod) -> MethodDocumentation:
        return MethodDocumentation(
            title=method.display_name or method.name,
            method_name=method.name,
            tags=method.tags,
            disabled=method.is_disabled,
            location=method.location
        )

    def _get_title(self, test_class: TestClass) -> str:
        return test_class.display_name or test_class.name

    def _get_class_name(self, test_class: TestClass) -> str:
        return test_class.name

    def _get_package(self, test_file: TestFile) -> str:
        return test_file.package or "(default)"

    def _render_title(self, title: str, class_name: str) -> list[str]:
        lines = []

        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"**Class:** `{class_name}`")
        lines.append("")

        return lines

    def _render_package(self, package: str) -> list[str]:
        lines = []

        lines.append(f"## Package")
        lines.append("")
        lines.append(f"{package}")
        lines.append("")

        return lines

    def _render_summary(self, summary: SummaryDocumentation) -> list[str]:
        lines = []

        lines.append(f"## Summary")
        lines.append("")
        lines.append(f"- Tests: {summary.tests}")
        lines.append(f"- Disabled: {summary.disabled}")
        lines.append(f"- Tagged: {summary.tagged}")

        return lines

    def _render_methods(self, methods: list[MethodDocumentation]) -> list[str]:
        lines = []

        lines.append(f"## Test Methods")
        lines.append("")

        for method in methods:
            lines.append(f"### {method.title}")
            lines.append("")
            lines.append(f"- Method: `{method.method_name}`")
            lines.append(f"- Tags: {", ".join(method.tags)}")
            lines.append(f"- Disabled: {"Yes" if method.disabled else "No"}")
            lines.append(f"- Source: {
                "Unknown" if method.location is None 
                else method.location.path + ":" + str(method.location.line)}"
            )

        return lines


