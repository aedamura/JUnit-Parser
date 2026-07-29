import os
import sys
from unittest import result

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)


from parser import JavaParser
from models import TestFile as SourceTestFile


def test_parser_reads_package_and_class(tmp_path):

    java_file = tmp_path / "UserTest.java"

    java_file.write_text(
        """
        package com.example.users;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.Tag;
        import org.junit.jupiter.api.DisplayName;

        @DisplayName("User Management Tests")
        class UserTest {

            @Test
            @Tag("user-management")
            @DisplayName("Creates a new user")
            void shouldCreateUser() {
            }
        }
        """
    )

    test_file = SourceTestFile(
        path=str(java_file)
    )

    parser = JavaParser()

    result = parser.parse(test_file)

    # --------
    # Package assertions
    # --------

    assert result.package == "com.example.users"

    # --------
    # Imports assertions
    # --------

    assert len(result.imports) == 3
    assert result.imports == [
        "org.junit.jupiter.api.Test",
        "org.junit.jupiter.api.Tag",     
        "org.junit.jupiter.api.DisplayName"   
    ]

    # --------
    # Class assertions
    # --------

    assert len(result.classes) == 1
    assert result.classes[0].name == "UserTest"
    assert result.classes[0].display_name == "User Management Tests"
    assert result.classes[0].annotations == ["DisplayName"]
    assert result.classes[0].tags == []
    

def test_parser_reads_methods_with_annotations(tmp_path):

    java_file = tmp_path / "UserTest.java"

    java_file.write_text(
        """
        package com.example.users;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.Tag;
        import org.junit.jupiter.api.DisplayName;

        class UserTest {

            @Test
            @Tag("user-management")
            @DisplayName("Creates a new user")
            void shouldCreateUser() {
            }
        }
        """
    )

    test_file = SourceTestFile(
        path=str(java_file)
    )

    parser = JavaParser()

    result = parser.parse(test_file)

    assert len(result.classes) == 1
    assert result.classes[0].name == "UserTest"
    assert len(result.classes[0].methods) == 1
    assert result.classes[0].methods[0].name == "shouldCreateUser"
    assert result.classes[0].methods[0].annotations == ["Test", "Tag", "DisplayName"]
    assert result.classes[0].methods[0].tags == ["user-management"]

def test_parser_reads_nested_classes(tmp_path):

    java_file = tmp_path / "UserTest.java"

    java_file.write_text(
        """
        package com.example.users;

        import org.junit.jupiter.api.Nested;
        import org.junit.jupiter.api.Test;

        class UserTest {

            @Nested
            class LoginTests {

                @Test
                void shouldLoginSuccessfully() {
                }

                @Nested
                class InvalidLoginTests {

                    @Test
                    void shouldFailWithInvalidCredentials() {
                    }
                }
            }

            class RegistrationTests {

                @Test
                void shouldRegisterSuccessfully() {
                }
            }
        }
        """
    )

    test_file = SourceTestFile(
        path=str(java_file)
    )

    parser = JavaParser()

    result = parser.parse(test_file)

    assert len(result.classes) == 1
    assert result.classes[0].name == "UserTest"

    root = result.classes[0]

    print(f"Root class: {root.name}, Nested classes: {[cls.name for cls in root.nested_classes]}")
    assert len(root.nested_classes) == 1
    nested = root.nested_classes[0]
    assert nested.name == "LoginTests"
    assert nested.annotations == ["Nested"]
    assert len(nested.methods) == 1
    assert nested.methods[0].name == "shouldLoginSuccessfully"


    assert len(nested.nested_classes) == 1
    sub_nested = nested.nested_classes[0]
    assert sub_nested.name == "InvalidLoginTests" 
    assert sub_nested.annotations == ["Nested"]
    assert len(sub_nested.methods) == 1
    assert sub_nested.methods[0].name == "shouldFailWithInvalidCredentials"
