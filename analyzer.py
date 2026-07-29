from models import Project, TestClass, TestMethod
from annotations import TEST_ANNOTATIONS, LIFECYCLE_ANNOTATIONS

class JUnitAnalyzer:

    def analyze(self, project: Project) -> Project:
        for test_file in project.test_files:

            for test_class in test_file.classes:

                self._analyze_class(test_class)

        return project

    def _analyze_class(self, test_class: TestClass):
        for method in test_class.methods:
            self._analyze_method(method)

        for nested in test_class.nested_classes:
            self._analyze_class(nested)

    def _analyze_method(self, test_method: TestMethod):
        annotations = set(test_method.annotations)

        test_method.is_test = bool(annotations & TEST_ANNOTATIONS)
        test_method.is_parameterized = "ParameterizedTest" in annotations
        test_method.is_disabled = "Disabled" in annotations

        for lifecycle in LIFECYCLE_ANNOTATIONS:
            if lifecycle in annotations:
                test_method.lifecycle = lifecycle
                break
