from analysis.analysis_models import DependencyGraph, CoverageReport, CoverageEntry

class CoverageAnalyzer:

    def analyze(self, dependency_graph: DependencyGraph) -> CoverageReport:
        coverage = []
        targets = []

        for dependency in dependency_graph.dependencies:
            if dependency.target in targets:
                index = targets.index(dependency.target)
                coverage[index].tests.append(dependency.source)
            else:
                targets.append(dependency.target)
                coverage.append(
                    CoverageEntry(dependency.target, [dependency.source])
                )

        for entry in coverage:
            entry.tests = sorted(entry.tests)

        return CoverageReport(
            entries=sorted(coverage, key=lambda entry: entry.target),
        )