import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from analysis.indexer import Indexer
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
                        qualified_name="com.example.users.UserTest",
                        nested_classes=[
                            TestClass(
                                name="LoginTests",
                                qualified_name="com.example.users.UserTest.LoginTests"
                            )
                        ]
                    )
                ]
            )
        ]
    )

    indexer = Indexer()
    indexer.index(project)

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