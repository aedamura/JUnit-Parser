from dependency_model import Dependency, DependencyGraph
from models import Project, TestClass, TestFile


class DependencyAnalyzer:

    def analyze(self, project: Project) -> DependencyGraph:
        graph = DependencyGraph()

        for test_file in project.test_files:
            self._analyze_file(test_file, graph)

        return graph

    def _analyze_file(self, test_file: TestFile, graph: DependencyGraph):
        lookup_table = self._build_lookup_table(test_file)

        for import_name in test_file.imports:
            if self._is_dependency(import_name):
                graph.add_dependency(
                    Dependency(
                        source=self._qualified_name(test_file, test_file.classes[0]),
                        target=import_name
                    )
                )

        for cls in test_file.classes:
            self._analyze_class(test_file, cls, lookup_table, graph)

    def _analyze_class(self, test_file: TestFile, test_class: TestClass, lookup_table: dict[str,str], graph: DependencyGraph):
        source = self._qualified_name(test_file, test_class)

        for field in test_class.fields:
            target = self._resolve_type(field.type, lookup_table)
            if self._is_dependency(target):

                graph.add_dependency(Dependency(source=source, target=target))

        for nested in test_class.nested_classes:
            self._analyze_class(test_file, nested, lookup_table, graph)

    def _build_lookup_table(self, test_file: TestFile) -> dict[str, str]:
        lookup = {}

        for import_name in test_file.imports:
            simple_name = import_name.split(".")[-1]

            lookup[simple_name] = import_name

        return lookup

    def _resolve_type(self, field_type: str, lookup: dict[str, str]) -> str:
        return lookup.get(field_type, field_type)

    def _is_dependency(self, import_name: str) -> bool:
        ignored_prefixes = (
            "java.",
            "javax.",
            "org.junit",
        )

        return not import_name.startswith(ignored_prefixes)

    def _qualified_name(self, test_file: TestFile, test_class: TestClass) -> str:
        if test_file.package:
            return f"{test_file.package}.{test_class.name}"

        return test_class.name