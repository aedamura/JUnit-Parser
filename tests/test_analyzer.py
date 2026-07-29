import os
import sys
from textwrap import dedent
from unittest import result

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)


from analyzer import JUnitAnalyzer
from models import TestMethod

def test_analyzer_stores_lifecycle():
    method_1 = TestMethod(
        name="testMethod",
        annotations=["BeforeEach"]
    )

    method_2 = TestMethod(
        name="testMethod2",
        annotations=["AfterEach"]
    )

    analyzer = JUnitAnalyzer()

    assert method_1.lifecycle is None

    analyzer._analyze_method(method_1)

    assert method_1.lifecycle == "BeforeEach"

    assert method_2.lifecycle is None

    analyzer._analyze_method(method_2)

    assert method_2.lifecycle == "AfterEach"

def test_analyzer_identifies_test_methods():
    method_1 = TestMethod(
        name="testMethod",
        annotations=["Test"]
    )

    method_2 = TestMethod(
        name="testMethod2",
        annotations=["ParameterizedTest"]
    )

    analyzer = JUnitAnalyzer()

    assert not method_1.is_test
    assert not method_1.is_parameterized

    analyzer._analyze_method(method_1)

    assert method_1.is_test
    assert not method_1.is_parameterized

    assert not method_2.is_test
    assert not method_2.is_parameterized

    analyzer._analyze_method(method_2)

    assert method_2.is_test
    assert method_2.is_parameterized