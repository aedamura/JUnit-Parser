from dataclasses import dataclass, field

from analysis.analysis_models import DependencyGraph
from models import SourceLocation

@dataclass
class MethodDocumentation:
    title: str
    method_name: str | None
    tags: list[str]
    disabled: bool
    location: SourceLocation | None

@dataclass
class SummaryDocumentation:
    tests: int = 0
    disabled: int = 0
    tagged: int = 0

@dataclass
class ClassDocumentation:
    title: str
    class_name: str
    package: str
    root_class: str
    dependencies: DependencyGraph
    summary: SummaryDocumentation
    methods: list[MethodDocumentation]
    nested_classes: list["ClassDocumentation"] = field(default_factory=list)

    def num_tests(self) -> int:
        x = len(self.methods)
        for nested in self.nested_classes:
            x += nested.num_tests()
        return x

    def num_disabled_tests(self) -> int:
        x = 0
        for method in self.methods:
            if method.disabled:
                x += 1

        for nested in self.nested_classes:
            x += nested.num_disabled_tests()
        return x

    def num_tagged_tests(self) -> int:
        x = 0
        for method in self.methods:
            if method.tags:
                x += 1

        for nested in self.nested_classes:
            x += nested.num_tagged_tests()
        return x

@dataclass
class ProjectDocumentation:
    packages: list[str]
    classes: list[ClassDocumentation]

