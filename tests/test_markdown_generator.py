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

    print(content)

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