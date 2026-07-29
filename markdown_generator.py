from pathlib import Path

from models import Project, TestClass, TestFile, TestMethod


class MarkdownGenerator:

    def generate(self, project: Project, output_dir: Path) -> None:

        output_dir.mkdir(parents=True, exist_ok=True)

        for test_file in project.test_files:

            for test_class in test_file.classes:

                self._write_class(test_file, test_class, output_dir)

    def _write_class(self, test_file: TestFile, test_class: TestClass, output_dir: Path):
        markdown = self._build_markdown(test_file, test_class)

        output_path = output_dir / (
            test_class.name + ".md"
        )

        output_path.write_text(markdown, encoding="utf-8")

    def _build_markdown(self, test_file: TestFile, test_class: TestClass) -> str:
        lines = []

        lines.extend(self._get_title(test_class))

        lines.extend(self._get_package(test_file))

        lines.extend(self._get_methods(test_class))

        return "\n".join(lines)

    def _get_title(self, test_class: TestClass) -> list[str]:
        lines = []

        title = test_class.display_name or test_class.name

        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"**Class:** `{test_class.name}`")
        lines.append("")

        return lines

    def _get_package(self, file: TestFile) -> list[str]:
        lines = []

        lines.append("## Package")
        lines.append("")
        lines.append(file.package or "(default)")
        lines.append("")

        return lines

    def _get_methods(self, test_class: TestClass) -> list[str]:
        lines = []

        lines.append("## Test Methods")
        for method in test_class.methods:
            if not method.is_test:
                continue

            lines.extend(self._get_method(method))

        return lines

    def _get_method(self, method: TestMethod) -> list[str]:
        lines = []

        lines.append(f"### {method.display_name or method.name}")
        lines.append("")

        lines.append(f"- Method: `{method.name}`")
        if method.tags:
            lines.append(
                "- Tags: "
                + ", ".join(method.tags)
            )

        lines.append(
            "- Disabled: "
            + ("Yes" if method.is_disabled else "No")
        )

        if method.location:
            lines.append(
                f"- Source "
                f"{Path(method.location.path).name}"
                f":{method.location.line}"
            )

        lines.append("")

        return lines