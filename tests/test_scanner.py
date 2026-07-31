import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from parsing.scanner import FileScanner

def test_scanner_finds_test_files(tmp_path):
    (tmp_path / "UserTest.java").write_text("")
    (tmp_path / "Helper.java").write_text("")

    scanner = FileScanner()

    project = scanner.scan(tmp_path)

    assert len(project.test_files) == 1
    assert project.test_files[0].path.endswith("UserTest.java")

