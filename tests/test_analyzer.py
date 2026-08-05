import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from analysis.analyzer import JUnitAnalyzer
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

    assert method_1.is_test is False
    assert method_1.is_parameterized is False
    assert method_1.is_disabled is False

    assert method_1.lifecycle is None

    analyzer._analyze_method(method_1)

    assert method_1.lifecycle == "BeforeEach"

    assert method_1.is_test is False
    assert method_1.is_parameterized is False
    assert method_1.is_disabled is False

    assert method_2.lifecycle is None

    analyzer._analyze_method(method_2)

    assert method_2.lifecycle == "AfterEach"

def test_analyzer_identifies_non_parameterized_test_methods():
    method = TestMethod(
        name="testMethod",
        annotations=["Test"]
    )

    analyzer = JUnitAnalyzer()

    assert not method.is_test
    assert not method.is_parameterized
    assert method.lifecycle is None
    assert not method.is_disabled

    analyzer._analyze_method(method)

    assert method.is_test
    assert not method.is_parameterized
    assert method.lifecycle is None
    assert not method.is_disabled

def test_analyzer_identifies_parameterized_test_methods():
    method = TestMethod(
        name="testMethod",
        annotations=["ParameterizedTest"]
    )

    analyzer = JUnitAnalyzer()

    assert not method.is_test
    assert not method.is_parameterized
    assert method.lifecycle is None
    assert not method.is_disabled

    analyzer._analyze_method(method)

    assert method.is_test
    assert method.is_parameterized
    assert method.lifecycle is None
    assert not method.is_disabled

def test_analyzer_identifies_disabled_methods():
    method = TestMethod(
        name="testMethod",
        annotations=["Disabled"]
    )

    analyzer = JUnitAnalyzer()

    assert not method.is_test
    assert not method.is_parameterized
    assert method.lifecycle is None
    assert not method.is_disabled

    analyzer._analyze_method(method)

    assert method.is_disabled
    assert not method.is_test
    assert not method.is_parameterized
    assert method.lifecycle is None