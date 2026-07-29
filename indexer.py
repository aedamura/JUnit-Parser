from models import Project, TestClass


class ProjectIndexer:

    def run(self, project: Project) -> Project:

        project.class_index.clear()

        for test_file in project.test_files:

            for test_class in test_file.classes:

                self._index_class(
                    project,
                    test_file.package or "",
                    test_class,
                    []
                )

        return project

    def _index_class(self, project: Project, package: str, test_class: TestClass, parents: list[str]):

        current_path = parents + [test_class.name]

        qualified_name = package + "." + ".".join(current_path)

        project.class_index[qualified_name] = test_class

        for nested in test_class.nested_classes:
            self._index_class(project, package, nested, current_path)