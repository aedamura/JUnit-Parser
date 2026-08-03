import os
import sys
from textwrap import dedent

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from analysis.project_analyzer import ProjectAnalyzer
from models import Project, TestFile, TestClass, TestMethod


def test_behaves_correctly():
    project = Project(
       test_files=[
           TestFile(
               path="path/to/file",
               classes=[
                   TestClass(
                       name="TestClassA",
                       qualified_name="TestClassA",
                       tags=["user"],
                       methods=[
                           TestMethod(
                               name="TestMethodA",
                               is_test=True,
                           ),
                           TestMethod(
                               name="TestMethodB",
                               is_test=True,
                               is_disabled=True
                           ),
                           TestMethod(
                               name="TestMethodC",
                               is_test=True,
                               is_parameterized=True
                           )
                       ],
                       nested_classes=[
                           TestClass(
                               name="TestClassAA",
                               qualified_name="TestClassAA",
                               methods=[
                                   TestMethod(
                                       name="TestMethodAA",
                                       is_test=True,
                                       tags=["unit"]
                                   ),
                                   TestMethod(
                                       name="TestMethodAB",
                                       is_test=True,
                                       tags=["unit"]
                                   ),
                                   TestMethod(
                                       name="TestMethodAC",
                                       is_test=True,
                                       is_disabled=False
                                   )
                               ],
                               nested_classes=[
                                   TestClass(
                                       name="TestClassAAA",
                                       qualified_name="TestClassAAA",
                                       methods=[
                                           TestMethod(
                                               name="TestMethodAAA",
                                               is_test=True
                                           ),
                                           TestMethod(
                                               name="TestMethodABA",
                                               is_test=False,
                                               is_disabled=True
                                           )
                                       ]
                                   )
                               ]
                           )
                       ]
                   ),
               ]
           ),
           TestFile(
               path="path/to/file",
               package="com.example.project",
               classes=[
                   TestClass(
                       name="TestClassB",
                       qualified_name="TestClassB",
                       methods=[
                           TestMethod(
                               name="TestMethodA",
                               is_test=True,
                               tags=["unit"]
                           ),
                           TestMethod(
                               name="TestMethodB",
                               is_test=True,
                               is_parameterized=True
                           ),
                           TestMethod(
                               name="TestMethodC",
                               is_test=False,
                           ),
                           TestMethod(
                               name="TestMethodD",
                               is_test=False,
                               lifecycle="BeforeEach"
                           )
                       ]
                   )
               ]
           )
       ]
    )

    result = ProjectAnalyzer().analyze(project)

    assert result.metrics.package_count == 2
    assert result.metrics.test_file_count == 2
    assert result.metrics.test_class_count == 4
    assert result.metrics.nested_class_count == 2
    assert result.metrics.test_method_count == 9
    assert result.metrics.parameterized_test_count == 2
    assert result.metrics.disabled_test_count == 1
    assert result.metrics.tagged_test_count == 3
    assert result.metrics.lifecycle_method_count == 1

