from dataclasses import dataclass, field
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
    summary: SummaryDocumentation
    methods: list[MethodDocumentation]
    nested_classes: list["ClassDocumentation"] = field(default_factory=list)

