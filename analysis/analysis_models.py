from dataclasses import dataclass, field

@dataclass
class Dependency:
    source: str
    target: str


@dataclass
class DependencyGraph:
    dependencies: list[Dependency] = field(default_factory=list)

    def add_dependency(self, dependency: Dependency):
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def dependencies_for(self, source: str) -> list[Dependency]:
        return [
            dependency
            for dependency in self.dependencies
            if dependency.source == source
        ]

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

@dataclass
class CoverageEntry:
    target: str
    tests: list[str]

@dataclass
class CoverageReport:
    entries: list[CoverageEntry]
