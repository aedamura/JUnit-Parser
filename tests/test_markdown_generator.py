import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from markdown_generator import MarkdownGenerator
from models import Project, TestFile, TestClass, SourceLocation, TestMethod

def test_generator_creates_markdown_file(tmp_path):
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
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

    output_directory = tmp_path / "docs"

    MarkdownGenerator().generate(project, output_directory)

    markdown_file = output_directory / "UserTest.md"

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
                        name="EmptyTest"
                    )
                ]
            )
        ]
    )

    output_dierctory = tmp_path / "docs"

    MarkdownGenerator().generate(project, output_dierctory)

    content = (
        output_dierctory / "EmptyTest.md"
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

    output_dierctory = tmp_path / "docs"

    MarkdownGenerator().generate(project, output_dierctory)

    content = (
        output_dierctory / "UserTest.md"
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

    output_dierctory = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, output_dierctory)

    content = (
        output_dierctory / "UserTest.md"
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

    output_dierctory = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, output_dierctory)

    content = (
        output_dierctory / "UserTest.md"
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
                                methods=[
                                    TestMethod(
                                        name="shouldLogin",
                                        is_test=True
                                    )
                                ],
                                nested_classes=[
                                    TestClass(
                                        name="ValidationTests",
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

    output_dierctory = tmp_path / "docs"
    
    MarkdownGenerator().generate(project, output_dierctory)

    content = (
        output_dierctory / "UserTest.md"
    ).read_text()

    print(content)

    assert "UserTest" in content
    assert "LoginTests" in content
    assert "shouldLogin" in content

def test_generator_creates_index_file(tmp_path):

    project = Project(
        test_files=[
            TestFile(
                path="UserTests.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTests",
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
                classes=[
                    TestClass(
                        name="OrderTests",
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

    generator = MarkdownGenerator()

    generator.generate(project, output_dir)

    index = output_dir / "index.md"

    assert index.exists()

    content = index.read_text()

    print(content)

    # ------------------------
    # Project Summary
    # ------------------------

    assert "# JUnit Test Documentation" in content

    assert "Package Count: 2" in content
    assert "Test Files: 2" in content
    assert "Test Classes: 3" in content
    assert "Test Methods: 4" in content
    assert "Disabled Tests: 1" in content

    # ------------------------
    # Packages
    # ------------------------

    assert "## Packages" in content

    assert "### com.example.users" in content
    assert "- [UserTests](UserTests.md)" in content
    assert "- [LoginTests](UserTests.md)" in content

    assert "### com.example.orders" in content
    assert "- [OrderTests](OrderTests.md)" in content