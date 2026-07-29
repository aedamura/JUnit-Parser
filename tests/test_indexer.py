import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from indexer import ProjectIndexer
from models import Project, TestClass, TestFile


def test_indexer():
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                classes=[
                    TestClass(
                        name="UserTest",
                        nested_classes=[
                            TestClass(
                                name="LoginTests"
                            )
                        ]
                    )
                ]
            )
        ]
    )

    indexer = ProjectIndexer()
    indexer.run(project)

    assert (
        "com.example.users.UserTest"
        in project.class_index
    )

    assert (
        "com.example.users.UserTest.LoginTests"
        in project.class_index
    )

    assert (
        project.class_index["com.example.users.UserTest"].name
        == "UserTest"
    )