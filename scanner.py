from pathlib import Path
from models import Project, TestFile

class FileScanner:

    def scan(self, root_path: str) -> Project:
        project = Project()

        root = Path(root_path)

        for file in root.rglob("*Test*.java"):
            if self._is_test_file(file):
                project.test_files.append(
                    TestFile(
                        path=str(file)
                    )
                )

        return project

    def _is_test_file(self, path: Path) -> bool:
        return path.name.endswith("Test.java") or path.name.startswith("Test")