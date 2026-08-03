from analysis.analysis_models import Dependency, DependencyGraph
from models import Project, TestClass, TestFile
from analysis.type_resolver import TypeResolver

class DependencyAnalyzer:

    def __init__(self):
        self._resolver = TypeResolver()

    def analyze(self, project: Project) -> DependencyGraph:
        graph = DependencyGraph()

        for test_file in project.test_files:
            self._analyze_file(test_file, graph, project)

        return graph

    def _analyze_file(self, test_file: TestFile, graph: DependencyGraph, project: Project):
        for import_name in test_file.imports:
            if self._is_dependency(import_name):
                graph.add_dependency(
                    Dependency(
                        source=test_file.classes[0].qualified_name,
                        target=import_name
                    )
                )

        for cls in test_file.classes:
            self._analyze_class(cls, test_file, graph, project)

    def _analyze_class(self, test_class: TestClass, test_file: TestFile, graph: DependencyGraph, project: Project):
        source = test_class.qualified_name

        for field in test_class.fields:
            target = self._resolver.resolve(field.type, test_file, project)
            if self._is_dependency(target):

                graph.add_dependency(Dependency(source=source, target=target))

        for nested in test_class.nested_classes:
            self._analyze_class(nested, test_file, graph, project)

    def _is_dependency(self, import_name: str) -> bool:
        ignored_prefixes = (
            "java.",
            "javax.",
            "org.junit",
        )

        return not import_name.startswith(ignored_prefixes)
