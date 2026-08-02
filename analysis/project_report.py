from dataclasses import dataclass, field

@dataclass
class ProjectMetrics:
    package_count: int
    test_file_count: int
    test_class_count: int
    nested_class_count: int
    test_method_count: int
    parameterized_test_count: int
    disabled_test_count: int
    tagged_test_count: int
    lifecycle_method_count: int

@dataclass
class ProjectReport:
    metrics: ProjectMetrics
