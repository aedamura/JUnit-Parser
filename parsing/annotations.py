TEST_ANNOTATIONS = {
    "Test",
    "ParameterizedTest",
    "RepeatedTest",
    "TestFactory"
}

LIFECYCLE_ANNOTATIONS = {
    "BeforeAll",
    "BeforeEach",
    "AfterAll",
    "AfterEach"
}

META_ANNOTATIONS = {
    "DisplayName",
    "Tag",
    "Disabled"
}

def is_test_annotation(annotation_name: str) -> bool:
    return annotation_name in TEST_ANNOTATIONS

def is_lifecycle_annotation(annotation_name: str) -> bool:
    return annotation_name in LIFECYCLE_ANNOTATIONS

def is_meta_annotation(annotation_name: str) -> bool:
    return annotation_name in META_ANNOTATIONS

def is_annotation(annotation_name: str) -> bool:
    return is_test_annotation(annotation_name) or is_lifecycle_annotation(annotation_name) or is_meta_annotation(annotation_name)