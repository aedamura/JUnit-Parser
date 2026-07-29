from pathlib import Path

from models import Project


class MarkdownGenerator:

    def generate(self, project: Project, output_dir: Path):
        ...