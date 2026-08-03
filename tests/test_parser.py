import os
import sys
from textwrap import dedent

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)


from parsing.parser import JavaParser
from models import TestClass, TestFile as SourceTestFile, TestMethod

FILE_CONTENTS = dedent("""\
    package com.example.users;

    import org.junit.jupiter.api.Nested;
    import org.junit.jupiter.api.Test;
    import org.junit.jupiter.api.TestFactory;
    import org.junit.jupiter.api.DisplayName;
    import org.junit.jupiter.api.Tag;
    
    import com.example.registration.RegistrationID;

    @DisplayName("User class behaves correctly")
    @Tag("feature")
    class UserTest {

        private UserService service;
        private UserRepository repository;

        UserTest(UserService service, UserRepository repository){
        }

        @DisplayName("User Login Tests")
        @Nested
        @Tag("login")
        @Tag("integration")
        class LoginTests {

            @DisplayName("Correct credentials logs the user in")
            @Test
            @Tag("login")
            void shouldLoginSuccessfully() {
            }

            @DisplayName("Users are limited to 5 incorrect password guesses")
            @ParameterizedTest
            @Tag("login")
            void hasLimitedPasswordAttempts(){
            }

            @DisplayName("Tests for invalid logins")
            @Nested
            class InvalidLoginTests {

                @DisplayName("Incorrect credentials do not log the user in")
                @Test
                @Tag("login")
                void shouldFailWithInvalidCredentials() {
                }
            }
        }

        @DisplayName("User Registration Tests")
        @Nested
        @Tag("registration")
        class RegistrationTests {

            private RegistrationID identifier;

            @DisplayName("User registers correctly")
            @ParameterizedTest
            @Tag("registraton")
            void shouldRegisterSuccessfully(User user, RegistrationID id) {
            }
        }

        @DisplayName("Helper Methods")
        class HelperMethods{
        
            @DisplayName("Produces the next userID")
            @Test
            void getUserID(){
            }

        }

        @DisplayName("Generate User Credentials")
        @BeforeEach
        @Tag("initialization")
        void initializeCredentials(){
        }
    }
""")

# -----------------
# Helper Methods
# -----------------

def _initialize_result(tmp_path) -> SourceTestFile:
    java_file = tmp_path / "UsersTest.java"
    java_file.write_text(FILE_CONTENTS)
    return JavaParser().parse(SourceTestFile(path=java_file))

def _get_top_level_class(test_file: SourceTestFile) -> TestClass:
    return test_file.classes[0]

def _get_class(class_name: str, class_list: list[TestClass]) -> TestClass:
    classes = []
    classes.extend(class_list)

    while len(classes) != 0:
        cls = classes.pop(0)
        classes.extend(cls.nested_classes)
        if cls.name == class_name:
            return cls

    return TestClass(name="Not Found", qualified_name="Not Found")

def _get_method(method_name: str, cls: TestClass) -> TestMethod:
    for method in cls.methods:
        if method.name == method_name:
            return method

    return TestMethod(name="Not Found")

# ----------
# Test Packages and Imports
# ----------

def test_parser_reads_package(tmp_path):
    result = _initialize_result(tmp_path)

    assert result.package == "com.example.users" 

def test_parser_reads_imports(tmp_path):
    result = _initialize_result(tmp_path)

    assert "com.example.registration.RegistrationID" in result.imports
    assert "org.junit.jupiter.api.Tag" in result.imports
    assert "org.junit.jupiter.api.Test" in result.imports
    assert "org.junit.jupiter.api.DisplayName" in result.imports

# ----------
# Test Class Level Parsing
# ----------

def test_parser_reads_top_level_class(tmp_path):
    result = _initialize_result(tmp_path)

    assert len(result.classes) == 1
    assert result.classes[0].name == "UserTest"

def test_parser_reads_tagged_nested_classes(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert len(cls.nested_classes) == 2

    nested = cls.nested_classes

    assert any(
        cls.name == "LoginTests"
        for cls in nested
    )
    
    assert any(
        cls.name == "RegistrationTests"
        for cls in nested
    )

    assert not any(
        cls.name == "InvalidLoginTests"
        for cls in nested
    )

    assert not any(
        cls.name == "HelperMethods"
        for cls in nested
    )

def test_parser_follows_nested_classes_tree(tmp_path):
    result = _initialize_result(tmp_path)

    assert len(result.classes) == 1
    assert len(result.classes[0].nested_classes) == 2
    assert result.classes[0].nested_classes[0].name == "LoginTests"
    assert len(result.classes[0].nested_classes[0].nested_classes) == 1
    assert result.classes[0].nested_classes[0].nested_classes[0].name == "InvalidLoginTests"
    assert len(result.classes[0].nested_classes[1].nested_classes) == 0

def test_parser_captures_correct_class_tags(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert len(cls.tags) == 1
    assert "feature" in cls.tags

    cls2 = _get_class("LoginTests", result.classes)

    assert len(cls2.tags) == 2
    assert "login" in cls2.tags
    assert "integration" in cls2.tags


def test_parser_captures_correct_class_annotations(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert "DisplayName" in cls.annotations
    assert "Tag" in cls.annotations

    cls = _get_class("LoginTests", result.classes)

    assert "Nested" in cls.annotations
    assert "DisplayName" in cls.annotations
    assert "Tag" in cls.annotations

def test_parser_captures_class_methods(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert len(cls.methods) == 1

    cls = _get_class("LoginTests", result.classes)

    assert len(cls.methods) == 2

def test_parser_captures_class_location(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert cls.location
    assert cls.location.line == 13

    cls = _get_class("LoginTests", result.classes)

    assert cls.location
    assert cls.location.line == 25

def test_parser_reads_class_fields(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert len(cls.fields) == 2

    assert cls.fields[0].name == "service"
    assert cls.fields[0].type == "UserService"
    assert cls.fields[0].location.line == 15

    assert cls.fields[1].name == "repository"
    assert cls.fields[1].type == "UserRepository"
    assert cls.fields[1].location.line == 16

    cls = _get_class("RegistrationTests", result.classes)

    assert len(cls.fields) == 1

    assert cls.fields[0].name == "identifier"
    assert cls.fields[0].type == "RegistrationID"
    assert cls.fields[0].location.line == 56

def test_parser_captures_constructors(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)

    assert len(cls.constructors) == 1
    constructor = cls.constructors[0]

    assert constructor.parameters == [
        "UserService",
        "UserRepository"
    ]
    assert constructor.location
    assert constructor.location.line == 18

# ----------
# Test Class Level Parsing
# ----------

def test_parser_captures_method_display_name(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)
    method = _get_method("initializeCredentials", cls)

    assert method.display_name == "Generate User Credentials"

def test_parser_captures_method_annotations(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)
    method = _get_method("initializeCredentials", cls)

    assert "DisplayName" in method.annotations
    assert "BeforeEach" in method.annotations
    assert "Tag" in method.annotations

def test_parser_captures_method_tags(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)
    method = _get_method("initializeCredentials", cls)

    assert "initialization" in method.tags

def test_parser_captures_method_location(tmp_path):
    result = _initialize_result(tmp_path)
    cls = _get_class("UserTest", result.classes)
    method = _get_method("initializeCredentials", cls)

    assert method.location
    assert method.location.line == 78

