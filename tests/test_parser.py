import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)


from parser import JavaParser
from models import TestFile as SourceTestFile


def test_parser_reads_package_and_class(tmp_path):

    java_file = tmp_path / "UserTest.java"

    java_file.write_text(
        """
        package com.example.users;

        import org.junit.jupiter.api.Test;

        class UserTest {
        }
        """
    )

    test_file = SourceTestFile(
        path=str(java_file)
    )

    parser = JavaParser()

    result = parser.parse(test_file)

    assert result.package == "com.example.users"
    assert result.imports == [
        "org.junit.jupiter.api.Test"
    ]
    assert len(result.classes) == 1
    assert result.classes[0].name == "UserTest"