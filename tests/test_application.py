import os
import sys
from textwrap import dedent

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from application import Application
from dependency_analyzer import DependencyAnalyzer
from dependency_generator import DependencyGraphGenerator
from indexer import Indexer
from markdown_generator import MarkdownGenerator
from parser import JavaParser
from pipline import Pipeline
from scanner import FileScanner


def test_application_generates_documentation(tmp_path):

    # -------------------------
    # Arrange
    # -------------------------

    source_dir = tmp_path / "java_project"
    output_dir = tmp_path / "docs"

    source_dir.mkdir()

    java_file = source_dir / "UserTest.java"

    java_file.write_text(
        dedent("""
        package com.example.users;

        import org.junit.jupiter.api.Test;

        class UserTest {

            @Test
            void shouldCreateUser() {
            }
        }
        """)
    )

    pipeline = Pipeline(
        FileScanner(),
        JavaParser(),
        Indexer()
    )

    application = Application(
        pipeline,
        MarkdownGenerator(),
        DependencyAnalyzer(),
        DependencyGraphGenerator()
    )

    project = pipeline.run(source_dir)

    assert len(project.test_files) == 1
    assert len(project.test_files[0].classes) == 1
    assert project.test_files[0].classes[0].name == "UserTest"

    # -------------------------
    # Act
    # -------------------------

    application.run(
        source_dir,
        output_dir
    )

    # -------------------------
    # Assert
    # -------------------------

    assert (output_dir / "index.md").exists()
    assert (output_dir / "UserTest.md").exists()
    assert (output_dir / "dependency_graph.md").exists()
    