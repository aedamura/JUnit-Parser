from models import Project

class JUnitAnalyzer:

    def analyze(self, project: Project) -> Project:
        for test_file in project.test_files:

            for test_class in test_file.classes:

                self._analyze_class(test_class)

        return project

    def _analyze_class(self, test_class):
        pass

    def _analyze_method(self, test_method):
        if "Test" in test_method.annotations:
            test_method.is_test = True

        elif "ParameterizedTest" in test_method.annotations:
            test_method.is_test = True
            test_method.is_parameterized = True

        elif "BeforeEach" in test_method.annotations:
            test_method.lifecycle = "BeforeEach"

        elif "AfterEach" in test_method.annotations:
            test_method.lifecycle = "AfterEach"