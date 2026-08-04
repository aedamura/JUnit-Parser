import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from analysis.analysis_models import DependencyGraph
from analysis.dependency_analyzer import DependencyAnalyzer
from documentation.documentation_generator import DocumentationGenerator
from models import Project, TestFile, TestClass, SourceLocation, TestMethod, Field

def _create_graph(project: Project) -> DependencyGraph:
    return DependencyAnalyzer().analyze(project)

def test_documentation_generator_creates_proper_documentation():
    project = Project(
        test_files=[
            TestFile(
                path="UserTest.java",
                package="com.example.users",
                imports=["com.example.repositories.UserRepository", "com.example.orders.Order",
                         "org.junit.jupiter.api.Test"],
                classes=[
                    TestClass(
                        name="UserTest",
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
                                        tags=["login"],
                                        is_test=True,
                                    )
                                ]
                            )
                        ],
                    )
                ],
            ),
            TestFile(
                path="OrderTest.java",
                package="com.example.orders",
                imports=["com.example.repositories.UserRepository", "com.example.users.User"],
                classes=[
                    TestClass(
                        name="OrderTest",
                        qualified_name="com.example.orders.OrderTest",
                        fields=[Field(type="UserRepository", name="name",
                                      location=SourceLocation("OrderTest.java", 16))],
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

    result = DocumentationGenerator().generate(project, dependency_graph=_create_graph(project))

    assert len(result.packages) == 2
    assert result.packages[0] == "com.example.orders"
    assert result.packages[1] == "com.example.users"

    assert len(result.classes) == 2
    assert result.classes[0].title == "OrderTest"
    assert result.classes[1].title == "UserTest"

    cls = result.classes[1]

    assert cls.summary.tests == 3
    assert cls.summary.disabled == 1
    assert cls.summary.tagged == 1

    assert len(cls.methods) == 2

    assert len(cls.nested_classes) == 1
    assert cls.nested_classes[0].title == "LoginTests"

    nested = cls.nested_classes[0]

    assert nested.summary.tests == 1
    assert nested.summary.disabled == 0
    assert nested.summary.tagged == 1


