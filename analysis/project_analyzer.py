from analysis.project_report import ProjectMetrics, ProjectReport
from models import Project, TestFile, TestClass, TestMethod


class ProjectAnalyzer:

    def __init__(self):
        self._packages = set()
        self._classes = []
        self._nested_classes = 0
        self._methods = 0
        self._tagged_methods = 0
        self._disabled_methods = 0
        self._parameterized_methods = 0
        self._lifecycle_methods = 0

    def analyze(self, project: Project) -> ProjectReport:

        for test_file in project.test_files:
            self._analyze_file(test_file)

        return ProjectReport(
            metrics=ProjectMetrics(
            package_count=len(self._packages),
            test_file_count=len(project.test_files),
            test_class_count=len(self._classes),
            nested_class_count=self._nested_classes,
            test_method_count= self._methods,
            parameterized_test_count= self._parameterized_methods,
            disabled_test_count= self._disabled_methods,
            tagged_test_count= self._tagged_methods,
            lifecycle_method_count= self._lifecycle_methods
            )
        )

    def _analyze_file(self, test_file: TestFile):
        self._packages.add(test_file.package)

        for test_class in test_file.classes:
            self._analyze_class(test_class)

    def _analyze_class(self, test_class: TestClass):
        self._classes.append(test_class)

        for method in test_class.methods:
            self._analyze_method(method)

        for nested_class in test_class.nested_classes:
            self._nested_classes += 1
            self._analyze_class(nested_class)

    def _analyze_method(self, test_method: TestMethod):
        if test_method.is_test:
            self._methods += 1
            if test_method.is_disabled:
                self._disabled_methods += 1
        if test_method.is_parameterized:
            self._parameterized_methods += 1
        if len(test_method.tags) > 0:
            self._tagged_methods += 1
        if test_method.lifecycle is not None:
            self._lifecycle_methods += 1