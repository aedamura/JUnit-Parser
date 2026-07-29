import javalang

from javalang.tree import ClassDeclaration, MethodDeclaration

from models import TestClass, TestFile, TestMethod

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
            test_class = TestClass(
                name= node.name
            )

            self._parse_methods(node, test_class)

            test_file.classes.append(test_class)

    def _parse_methods(self, class_node, test_class: TestClass):

        for method in class_node.methods:
            test_method = TestMethod(
                name=method.name
            )

            self._parse_annotations(method, test_method)

            test_class.methods.append(test_method)

    def _parse_annotations(self, method_node, target: TestMethod):
        for annotation in method_node.annotations:
            target.annotations.append(annotation.name)

            if annotation.name == "Tag":
                value = self._get_annotation_value(annotation)

                if value:
                    target.tags.append(value)

            elif annotation.name == "DisplayName":
                value = self._get_annotation_value(annotation)

                if value:
                    target.display_name = value

    def _get_annotation_value(self, annotation):
        if annotation.element is None:
            return None

        return annotation.element.value.strip('"')