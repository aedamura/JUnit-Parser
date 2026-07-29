from dataclasses import dataclass, field

@dataclass
class SourceLocation:
    path: str
    line: int

@dataclass
class TestMethod:
    name: str
    display_name: str | None = None

    annotations: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    method_parameters: list[str] = field(default_factory=list)
    
    is_test: bool = False
    is_parameterized: bool = False
    lifecycle: str | None = None
    is_disabled: bool = False

    location: SourceLocation | None = None

@dataclass
class TestClass:
    name: str
    display_name: str | None = None
    annotations: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    methods: list[TestMethod] = field(default_factory=list)
    nested_classes: list["TestClass"] = field(default_factory=list)
    location: SourceLocation | None = None

@dataclass
class TestFile:
    path: str
    package: str | None = None
    imports: list[str] = field(default_factory=list)
    classes: list[TestClass] = field(default_factory=list)

@dataclass
class Project:
    test_files: list[TestFile] = field(default_factory=list)

    class_index: dict[str, TestClass] = field(default_factory=dict)