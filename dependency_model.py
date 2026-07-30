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
            self.add_dependency(dependency)