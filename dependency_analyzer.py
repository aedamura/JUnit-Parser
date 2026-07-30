from dependency_model import Dependency, DependencyGraph
from models import Project, TestClass, TestFile


class DependencyAnalyzer:

    def analyze(self, project: Project) -> DependencyGraph:
        graph = DependencyGraph()

        for test_file in project.test_files:
            for test_class in test_file.classes:
                self._analyze_class(test_file, test_class, graph) 

        return graph

    def _analyze_class(self, test_file: TestFile, test_class: TestClass, graph: DependencyGraph):
        source = test_file.package + "." + test_class.name

        for import_name in test_file.imports:
            if self._is_dependency(import_name):

                graph.dependencies.append(
                    Dependency(source=source, target=import_name)
                )

            for nested in test_class.nested_classes:
                self._analyze_class(test_file, nested, graph)

    def _is_dependency(self, import_name: str) -> bool:
        ignored = [
            "org.junit.",
            "java.",
            "javax."
        ]

        return not any(
            import_name.startswith(prefix)
            for prefix in ignored
        )