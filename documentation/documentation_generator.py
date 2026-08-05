from analysis.analysis_models import DependencyGraph
from documentation.markdown_models import ProjectDocumentation, ClassDocumentation, MethodDocumentation, \
    SummaryDocumentation
from models import Project, TestClass, TestMethod


class DocumentationGenerator:

    def generate(self, project: Project, dependency_graph: DependencyGraph) -> ProjectDocumentation:
        packages = []
        classes = []

        for test_file in project.test_files:
            if test_file.package not in packages:
                packages.append(test_file.package)

            for cls in test_file.classes:
                classes.append(self._create_class_doc(cls, dependency_graph, test_file.package, cls.name))

        return ProjectDocumentation(
            packages=sorted(packages),
            classes=sorted(classes, key=lambda x: (x.package, x.class_name)),
        )

    def _create_class_doc(self, test_class: TestClass, dependency_graph: DependencyGraph, package: str, root_class_name: str) -> ClassDocumentation:

        nested = [
            self._create_class_doc(
                nested_class,
                DependencyGraph(dependency_graph.dependencies_for(test_class.qualified_name)),
                package,
                root_class_name
            ) for nested_class in test_class.nested_classes
        ]

        methods = [
            self._create_method_doc(
                method
            ) for method in test_class.methods
            if method.is_test
        ]

        summary = self._create_class_summary(nested, methods)

        return ClassDocumentation(
           title=self._get_title(test_class),
            class_name=test_class.name,
            package=package,
            root_class=root_class_name,
            dependencies=DependencyGraph(dependency_graph.dependencies_for(test_class.qualified_name)),
            summary=summary,
            methods=methods,
            nested_classes=nested
        )

    def _create_method_doc(self, test_method: TestMethod) -> MethodDocumentation:
        return MethodDocumentation(
            title=self._get_title(test_method),
            method_name=test_method.name,
            tags=test_method.tags,
            disabled=test_method.is_disabled,
            location=test_method.location,
        )

    def _create_class_summary(self, nested: list[ClassDocumentation], methods: list[MethodDocumentation]) -> SummaryDocumentation:
        tests = 0
        disabled = 0
        tagged = 0

        for method in methods:
            tests += 1
            if method.disabled:
                disabled += 1
            if method.tags:
                tagged += 1

        for cls in nested:
            tests += cls.num_tests()
            disabled += cls.num_disabled_tests()
            tagged += cls.num_tagged_tests()

        return SummaryDocumentation(
            tests=tests,
            disabled=disabled,
            tagged=tagged,
        )

    # --------------------
    # Helper Functions
    # --------------------

    def _get_title(self, test_class) -> str:
        return test_class.display_name or test_class.name

