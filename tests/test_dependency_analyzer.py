import os
import sys
from textwrap import dedent


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from analysis.dependency_analyzer import DependencyAnalyzer
from analysis.dependency_model import DependencyGraph, Dependency
from models import Project, TestFile as SourceTestFile
from parsing.parser import JavaParser

def _parse(file) -> Project:
    return Project(
        test_files=[
            JavaParser().parse(SourceTestFile(path=file))
        ]
    )

def _build_graph(file) -> DependencyGraph:
    return DependencyAnalyzer().analyze(_parse(file))

def test_dependency_analyzer_identifies_imports(tmp_path):
    java_file = tmp_path / "UserTest.java"

    java_file.write_text(dedent("""\
        package com.example.users;

        import com.example.UserService;

        class UserTest{}
    """))

    graph = _build_graph(java_file) 

    assert len(graph.dependencies) == 1
    assert graph.dependencies[0].source == "com.example.users.UserTest"
    assert graph.dependencies[0].target == "com.example.UserService"

def test_dependency_analyzer_ignores_junit_imports(tmp_path):
    java_file = tmp_path / "UserTest.java"

    java_file.write_text(dedent("""\
        package com.example.users;

        import com.example.UserService;
        import org.example.Test;
        import org.junit.jupiter.api.Tag;

        class UserTest{}
    """))

    graph = _build_graph(java_file)

    assert len(graph.dependencies) == 2
    assert not any(
        dependency.source.startswith("org.junit.")
        for dependency in graph.dependencies
    )

def test_dependency_analyzer_ignores_java_imports(tmp_path):
    java_file = tmp_path / "UserTest.java"

    java_file.write_text(dedent("""\
        package com.example.users;

        import com.example.UserService;
        import java.example.Test;
        import javax.example.Utils;

        class UserTest{}
    """))

    graph = _build_graph(java_file)

    assert len(graph.dependencies) == 1
    assert not any(
        dependency.source.startswith("java." or "javax.")
        for dependency in graph.dependencies
    )

def test_dependency_analyzer_captures_fields(tmp_path):
    java_file = tmp_path / "UserTest.java"

    java_file.write_text(dedent("""\
        package com.example.users;

        class UserTest{
            private User user;
            private Register register;
        }
    """))

    graph = _build_graph(java_file)

    assert len(graph.dependencies) == 2
    assert any(
        dependency.target == "com.example.users.User"
        for dependency in graph.dependencies
    )

    assert any(
        dependency.target == "com.example.users.Register"
        for dependency in graph.dependencies
    )

def test_source_and_target_are_properly_labeled(tmp_path):
    java_file = tmp_path / "UserTest.java"

    java_file.write_text(dedent("""\
        package com.example.users;

        import com.example.UserService;

        class UserTest{
            private User user;
        }
    """))

    graph = _build_graph(java_file)

    assert len(graph.dependencies) == 2

    assert all(
       dependency.source == "com.example.users.UserTest"
       for dependency in graph.dependencies 
    )
    assert any(
        dependency.target == "com.example.UserService"
        for dependency in graph.dependencies
    )  
    assert any(
        dependency.target == "com.example.users.User"
        for dependency in graph.dependencies
    )

def test_dependency_model_functions():
    graph = DependencyGraph([
        Dependency(
            source="com.example.users.UserTest",
            target="com.example.User"
        )
    ])

    dp = graph.dependencies_for("com.example.users.UserTest")

    assert len(dp) == 1
    assert dp[0].target == "com.example.User"
