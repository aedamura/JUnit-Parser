from models import Project, TestFile

JAVA_SIMPLE_TYPES = {
    "String",
    "Object",
    "Integer",
    "Long",
    "Short",
    "Byte",
    "Boolean",
    "Character",
    "Double",
    "Float",
    "Void",

    "List",
    "Set",
    "Map",
    "Queue",
    "Deque",

    "Optional",

    "Collection",
    "Iterable",

    "ArrayList",
    "HashMap",
    "HashSet",

    "Stream"
}

class TypeResolver:

    def resolve(
            self,
            type_name: str,
            test_file: TestFile,
            project: Project
    ) -> str:
        if type_name in project.class_index:
            return type_name
        
        for imported in test_file.imports:
            if imported.endswith("." + type_name) and imported in project.class_index:
                return imported

        if type_name in JAVA_SIMPLE_TYPES:
            return type_name

        return test_file.package + "." + type_name

        