import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from analysis.analysis_models import DependencyGraph, Dependency
from analysis.coverage_analyzer import CoverageAnalyzer


def test_coverage_analyzer_produces_test_report():
    dependency_graph = DependencyGraph(
        dependencies=[
            Dependency(
                source="UserTest",
                target="UserRepository"
            ),
            Dependency(
                source="UserTest",
                target="Orders"
            ),
            Dependency(
                source="UserTest",
                target="Users"
            ),
            Dependency(
                source="OrderTest",
                target="Orders"
            ),
        ]
    )

    coverage = CoverageAnalyzer().analyze(dependency_graph)

    assert len(coverage.entries) == 3
    assert coverage.entries[0].target == "Orders"
    assert len(coverage.entries[0].tests) == 2
    assert coverage.entries[0].tests[0] == "OrderTest"
    assert coverage.entries[0].tests[1] == "UserTest"
    assert coverage.entries[1].target == "UserRepository"
    assert len(coverage.entries[1].tests) == 1