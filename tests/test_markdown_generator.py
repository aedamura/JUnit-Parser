import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from analysis.dependency_analyzer import DependencyAnalyzer
from analysis.dependency_model import DependencyGraph
from documentation.markdown_generator import MarkdownGenerator
from models import Project, TestFile, TestClass, SourceLocation, TestMethod, Field
from analysis.project_analyzer import ProjectAnalyzer
from analysis.project_report import ProjectReport

def _create_graph(project: Project) -> DependencyGraph:
    return DependencyAnalyzer().analyze(project)

def _create_report(project: Project) -> ProjectReport:
    return ProjectAnalyzer().analyze(project)

def test_generator_creates_markdown_file(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        display_name="User Management Tests",
                        methods=[
                            TestMethod(
                                name="shouldCreateUser",
                                display_name="Creates a new user",
                                is_test=True,
                                tags=["user-management"],
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=14
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"

    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    markdown_file = output_dir / "UserTest.md"

    assert markdown_file.exists()

    content = markdown_file.read_text()

    assert "# User Management Tests" in content
    assert "**Class:** `UserTest`" in content
    assert "## Test Methods" in content
    assert "Creates a new user" in content
    assert "user-management" in content
    assert "UserTest.java:14" in content

def test_generator_handles_empty_test_class(tmp_path):

    project = Project(
        test_files=[
            TestFile(
                path="EmptyTest.java",
                package="com.example",
                classes=[
                    TestClass(
                        name="EmptyTest",
                        qualified_name="com.example.EmptyTest"
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"

    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "EmptyTest.md"
    ).read_text()

    assert "# EmptyTest" in content

def test_generator_only_lists_tests(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        display_name="User Management Tests",
                        methods=[
                            TestMethod(
                                name="shouldCreateUser",
                                display_name="Creates a new user",
                                is_test=True,
                                is_disabled=False,
                                tags=["user-management"],
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=14
                                )
                            ),
                            TestMethod(
                                name="setup",
                                display_name="Sets up unit tests",
                                is_test=False,
                                tags=["user-management"],
                                lifecycle="BeforeEach",
                                is_disabled=False,
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=32
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"

    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "UserTest.md"
    ).read_text()


    assert "shouldCreateUser" in content
    assert not "setup" in content

def test_generator_produces_correct_summary(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        display_name="User Management Tests",
                        methods=[
                            TestMethod(
                                name="shouldCreateUser",
                                display_name="Creates a new user",
                                is_test=True,
                                is_disabled=False,
                                tags=["user-management"],
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=14
                                )
                            ),
                            TestMethod(
                                name="setup",
                                display_name="Sets up unit tests",
                                is_test=False,
                                tags=["user-management"],
                                lifecycle="BeforeEach",
                                is_disabled=False,
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=32
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "UserTest.md"
    ).read_text()


    assert "- Tests: 1" in content
    assert "- Disabled: 0" in content
    assert "- Tagged: 1" in content

def test_generator_handles_nested_classes(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        display_name="User Management Tests",
                        methods=[
                            TestMethod(
                                name="shouldCreateUser",
                                display_name="Creates a new user",
                                is_test=True,
                                is_disabled=False,
                                tags=["user-management"],
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=14
                                )
                            ),
                            TestMethod(
                                name="setup",
                                display_name="Sets up unit tests",
                                is_test=False,
                                tags=["user-management"],
                                lifecycle="BeforeEach",
                                is_disabled=False,
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=32
                                )
                            )
                        ],
                        nested_classes=[
                            TestClass(
                                name="LoginTests",
                                qualified_name="com.example.users.UserTest.LoginTests",
                                    methods=[
                                    TestMethod(
                                        name="shouldLogin",
                                        is_test=True
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "UserTest.md"
    ).read_text()

    assert "UserTest" in content
    assert "LoginTests" in content
    assert "shouldLogin" in content

def test_generator_handles_nested_inner_classes(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        display_name="User Management Tests",
                        methods=[
                            TestMethod(
                                name="shouldCreateUser",
                                display_name="Creates a new user",
                                is_test=True,
                                is_disabled=False,
                                tags=["user-management"],
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=14
                                )
                            ),
                            TestMethod(
                                name="setup",
                                display_name="Sets up unit tests",
                                is_test=False,
                                tags=["user-management"],
                                lifecycle="BeforeEach",
                                is_disabled=False,
                                location=SourceLocation(
                                    path="UserTest.java",
                                    line=32
                                )
                            )
                        ],
                        nested_classes=[
                            TestClass(
                                name="LoginTests",
                                qualified_name="com.example.users.UserTest.LoginTests",
                                methods=[
                                    TestMethod(
                                        name="shouldLogin",
                                        is_test=True
                                    )
                                ],
                                nested_classes=[
                                    TestClass(
                                        name="ValidationTests",
                                qualified_name="com.example.users.UserTest.LoginTests.ValidationTests",
                                        methods=[
                                            TestMethod(
                                                name="shouldValidate",
                                                is_test=True
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    output_dir = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "UserTest.md"
    ).read_text()

    assert "UserTest" in content
    assert "LoginTests" in content
    assert "shouldLogin" in content

def test_generator_creates_index_file(tmp_path):

    project = Project(
        test_files=[
            TestFile(
                path="UserTests.java",
                package="com.example.users",
                imports=["com.example.repositories.UserRepository", "com.example.orders.Order", "org.junit.jupiter.api.Test"],
                classes=[
                    TestClass(
                        name="UserTests",
                        qualified_name="com.example.users.UserTest",
                        fields=[Field(type="User", name="name", location=SourceLocation("UserTest.java", 8))],
                        methods=[
                            TestMethod(
                                name="shouldLogin",
                                is_test=True,
                            ),
                            TestMethod(
                                name="shouldDelete",
                                is_test=True,
                                is_disabled=True,
                            ),
                        ],
                        nested_classes=[
                            TestClass(
                                name="LoginTests",
                                qualified_name="com.example.users.UserTest.LoginTests",
                                methods=[
                                    TestMethod(
                                        name="shouldValidatePassword",
                                        is_test=True,
                                    )
                                ]
                            )
                        ],
                    )
                ],
            ),
            TestFile(
                path="OrderTests.java",
                package="com.example.orders",
                imports=["com.example.repositories.UserRepository", "com.example.users.User"],
                classes=[
                    TestClass(
                        name="OrderTest",
                        qualified_name="com.example.orders.OrderTest",
                        fields=[Field(type="UserRepository", name="name", location=SourceLocation("OrderTest.java", 16))],
                        methods=[
                            TestMethod(
                                name="shouldCreateOrder",
                                is_test=True,
                            )
                        ],
                    )
                ],
            ),
        ]
    )

    output_dir = tmp_path / "docs"

    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    index = output_dir / "index.md"

    assert index.exists()

    content = index.read_text()
    print(content)

    # ------------------------
    # Project Summary
    # ------------------------

    assert "# JUnit Test Documentation" in content

    assert "Packages: 2" in content
    assert "Test Files: 2" in content
    assert "Test Classes: 3" in content
    assert "Test Methods: 4" in content
    assert "Disabled Tests: 1" in content

    # ------------------------
    # Dependency Graph
    # ------------------------

    assert "## Dependency Graph" in content

    assert "```mermaid" in content
    assert "com.example.users.UserTest --> com.example.repositories.UserRepository" in content
    assert "com.example.users.UserTest --> com.example.users.User" in content
    assert "com.example.orders.OrderTest --> com.example.repositories.UserRepository" in content
    assert "com.example.orders.OrderTest --> com.example.users.User" in content

    # ------------------------
    # Packages
    # ------------------------

    assert "## Packages" in content

    assert "### com.example.users" in content
    assert "- [UserTests](UserTests.md)" in content
    assert "- [LoginTests](UserTests.md)" in content

    assert "### com.example.orders" in content
    assert "[OrderTest](OrderTest.md)" in content

def test_generator_creates_dependencies(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                imports=["com.example.UserRepository", "com.example.UserRequirements", "org.junit.jupiter.api.Test"],
                classes=[
                    TestClass(
                        name="UserTest",
                        qualified_name="com.example.users.UserTest",
                        fields=[
                            Field(
                                name="user",
                                type="User",
                                location=SourceLocation("UserTest.java", 13)
                            ),
                            Field(
                                name="repository",
                                type="UserRepository",
                                location=SourceLocation("UserTest.java", 13)
                            )
                        ],
                        methods=[
                            TestMethod(
                                name="shouldLoginSuccessfully"
                            )
                        ]
                    )
                ],
            ),
        ]
    )


    output_dir = tmp_path / "docs"
    
    graph = _create_graph(project)
    #print(graph)

    MarkdownGenerator().generate(project, _create_graph(project), _create_report(project), output_dir)

    content = (
        output_dir / "UserTest.md"
    ).read_text()

    #print(content)
    
    assert "## Dependencies" in content

    assert "### List" in content
    assert "- com.example.UserRepository" in content
    assert "- com.example.UserRequirements" in content
    assert "- com.example.users.User" in content
    assert "- org.junit.jupiter.api.Test" not in content

    assert "### Graph" in content
    assert "```mermaid" in content
    assert "UserTest --> UserRepository" in content
    assert "UserTest --> UserRequirements" in content
    assert "UserTest --> User" in content
    assert "UserTest --> Test" not in content

