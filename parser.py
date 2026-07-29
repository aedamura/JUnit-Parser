import javalang

from javalang.tree import ClassDeclaration

from models import TestClass, TestFile

class JavaParser:

    def parse(self, test_file: TestFile) -> TestFile:
        with open(test_file.path, "r", encoding="utf-8") as file:
            source = file.read()

        tree = javalang.parse.parse(source)

        self._parse_package(tree, test_file)
        self._parse_imports(tree, test_file)
        self._parse_classes(tree, test_file)

        return test_file

    def _parse_package(self, tree, test_file: TestFile):
        if tree.package:
            test_file.package = tree.package.name

    def _parse_imports(self, tree, test_file: TestFile):
        test_file.imports = [
            import_decl.path
            for import_decl in tree.imports
        ]

    def _parse_classes(self, tree, test_file: TestFile):
        for _, node in tree.filter(ClassDeclaration):
            test_file.classes.append(
                TestClass(
                    name = node.name
                )
            )