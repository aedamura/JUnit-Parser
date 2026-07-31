class MarkdownWriter:

    def __init__(self):
        self._lines = []

    def heading (self, level: int, text):
        self._lines.append("#" * level + " " + str(text))
        self.blank_line()

    def line(self, text):
        self._lines.append(str(text))

    def bullet(self, text, indents: int=0):
        self._lines.append("  "*indents + "- " + str(text))

    def code_block(self, language: str, text):
        self._lines.append(f"```{language}")
        self._lines.append(str(text))
        self._lines.append("```")
        self.blank_line()

    def horizontal_rule(self):
        self._lines.append("---")
        self.blank_line()

    def section(self, text):
        self._lines.append(str(text))

    def blank_line(self):
        self._lines.append("")

    def build(self) -> str:
        return "\n".join(self._lines)