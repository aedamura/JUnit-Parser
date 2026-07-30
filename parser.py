import javalang

from javalang.tree import ClassDeclaration, MethodDeclaration
from annotations import (
    is_test_annotation,
    is_lifecycle_annotation,
    is_meta_annotation
)
from models import Constructor, SourceLocation, TestClass, TestFile, TestMethod, Field

class JavaParser:

    def parse(self, test_file: TestFile) -> TestFile:
        with open(test_file.path, "r", encoding="utf-8") as file:
            source = file.read()

        tree = javalang.parse.parse(source)

        self._parse_package(tree, test_file)
        self._parse_imports(tree, test_file)
        self._parse_classes(tree, test_file)

        return test_file

    # ----------
    # FILE LEVEL PARSERS
    # ----------

    def _parse_package(self, tree, test_file: TestFile):
        if tree.package:
            test_file.package = tree.package.name

    def _parse_imports(self, tree, test_file: TestFile):
        test_file.imports = [
            import_decl.path
            for import_decl in tree.imports
        ]

    def _parse_classes(self, tree, test_file: TestFile):
        for type_decl in tree.types:
            if isinstance(type_decl, ClassDeclaration):
                test_class = self._create_test_class(type_decl, test_file.path)

                test_file.classes.append(test_class)

    # ----------
    # CLASS LEVEL PARSERS
    # ----------

    def _parse_nested_classes(self, node, file_path, test_class: TestClass):

        for nested in node.body:
            if isinstance(nested, ClassDeclaration) and self._has_annotation(nested, "Nested"):
                nested_class = self._create_test_class(nested, file_path)
                test_class.nested_classes.append(nested_class)

    def _parse_methods(self, class_node, test_class: TestClass, file_path: str):

        for method in class_node.methods:
            test_method = TestMethod(
                name=method.name,
                location= self._create_location(method, file_path)
            )

            self._parse_annotations(method, test_method)

            test_class.methods.append(test_method)

    def _parse_annotations(self, method_node, target):
        for annotation in method_node.annotations:
            target.annotations.append(annotation.name)

            value  = self._get_annotation_value(annotation)

            if annotation.name == "Tag" and value:
                target.tags.append(value)

            elif annotation.name == "DisplayName" and value:
                target.display_name = value

    def _parse_fields(self, class_node, test_class: TestClass, file_path: str):
        for field in class_node.fields:

            field_type = field.type.name

            for declarator in field.declarators:

                test_class.fields.append(
                    Field(
                        name=declarator.name,
                        type=field_type,
                        location= self._create_location(field, file_path)
                    )
                )

    def _parse_constructors(self, class_node, test_class: TestClass, file_path: str):
        for constructor in class_node.constructors:
            params = []

            for param in constructor.parameters:

                params.append(
                    param.type.name
                )

            test_class.constructors.append(
                Constructor(
                    parameters = params,
                    location = self._create_location(constructor, file_path)
                )
            )



    # ----------
    # OBJECT CONSTRUCTORS
    # ----------

    def _create_test_class(self, node, file_path: str) -> TestClass:
        test_class = TestClass(
            name=node.name,
            location= self._create_location(node, file_path)
        )

        self._parse_annotations(node, test_class)
        self._parse_fields(node, test_class, file_path)
        self._parse_constructors(node, test_class, file_path)
        self._parse_methods(node, test_class, file_path)
        self._parse_nested_classes(node, file_path, test_class)

        return test_class

    def _create_location(self, node, file_path: str) -> SourceLocation:
        return SourceLocation(
            path=file_path,
            line=node.position.line
        )

    # ----------
    # MISC HELPER FUNCTIONS
    # ----------
    
    def _has_annotation(self, node, annotation_name: str) -> bool:
        return any(
            annotation.name == annotation_name
            for annotation in node.annotations
        )

    def _get_annotation_value(self, annotation):
        if annotation.element is None:
            return None

        return annotation.element.value.strip('"')
