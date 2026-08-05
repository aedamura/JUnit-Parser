import os
import sys
from textwrap import dedent

from analysis.project_analyzer import ProjectAnalyzer
from documentation.documentation_generator import DocumentationGenerator

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from application import Application
from analysis.dependency_analyzer import DependencyAnalyzer
from analysis.coverage_analyzer import CoverageAnalyzer
from analysis.indexer import Indexer
from analysis.analyzer import JUnitAnalyzer
from documentation.markdown_generator import MarkdownGenerator
from parsing.parser import JavaParser
from pipline import Pipeline
from parsing.scanner import FileScanner

def test_application_generates_documentation(tmp_path):

    # -------------------------
    # Arrange
    # -------------------------

    source_dir = tmp_path / "java_project"
    output_dir = tmp_path / "docs"

    source_dir.mkdir()

    test_dir = source_dir / "test"
    test_dir.mkdir()
    java_dir = test_dir / "java"
    java_dir.mkdir()

    com_dir = java_dir / "com"
    com_dir.mkdir()
    example_dir = com_dir / "example"
    example_dir.mkdir()
    users_dir = example_dir / "users"
    users_dir.mkdir()

    user_test = users_dir / "UserTest.java"
    user_test.write_text(
        dedent("""
        package com.example.users;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.Tag;
        import org.junit.jupiter.api.DisplayName;
        import org.junit.jupiter.api.Nested;

        import com.example.repositories.UserRepository;
        import com.example.orders.Order;

        class UserTest {

            private UserRepository repository;
            private User user;

            @DisplayName("Users can be created")
            @Test
            @Tag("user")
            @Tag("unit")
            void shouldCreateUser() {
            }

            @Nested
            class LoginTests{
            
                @DisplayName("User logs in with the proper credentials")
                @Test
                @Tag("user")
                @Tag("user-login")
                @Tag("unit")
                void userLoginSuccessfully(){
                }

                @DisplayName("User can't login after 5 failed password attempts")
                @Test
                @Tag("user")
                @Tag("user-login")
                @Tag("unit")
                void loginLocksAfterRepeatedFails(){
                }
            }

        }
        """)
    )

    user_repository_test = users_dir / "UserRepositoryTest.java"
    user_repository_test.write_text(dedent("""\
        package com.example.users;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.DisplayName;
        import org.junit.jupiter.api.Tag;
        import org.junit.jupiter.api.Nested;

        import com.example.repositories.UserRepository;
        
        class UserRepositoryTest{
        
            private UserRepository repository;

            @DisplayName("Users can be added to the repository")
            @Test
            @Tag("user-repository")
            @Tag("unit")
            void usersAreAddedToRepository(){
            }
        }

    """))

    orders_dir = example_dir / "orders"
    orders_dir.mkdir()

    order_test = orders_dir / "OrderTest.java"
    order_test.write_text(dedent("""\
        package com.example.orders;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.DisplayName;
        import org.junit.jupiter.api.Nested;
        import org.junit.jupiter.api.Tag;

        import com.example.repositories.OrderRepository;
        import com.example.users.User;

        class OrderTest{
        
            private OrderRepository repository;
            private User user;
            private Order order;

            @DisplayName("Orders can be created")
            @Test
            @Tag("order")
            @Tag("unit")
            void shouldCreateOrder(){
            }

            @DisplayName("Created orders are added to the repository")
            @Test
            @Tag("order")
            @Tag("unit")
            void shouldAddOrderToRepository(){
            }
        }

    """))

    

    pipeline = Pipeline(
        scanner=FileScanner(),
        parser=JavaParser(),
        analyzer=JUnitAnalyzer(),
        indexer=Indexer()
    )

    application = Application(
        pipeline=pipeline,
        markdown_generator=MarkdownGenerator(),
        project_analyzer=ProjectAnalyzer(),
        dependency_analyzer=DependencyAnalyzer(),
        documentation_generator=DocumentationGenerator(),
        coverage_analyzer=CoverageAnalyzer()
    )

    project = pipeline.run(test_dir)
    print(project)

    # -------------------------
    # Act
    # -------------------------

    application.run(
        test_dir,
        output_dir
    )

    # -------------------------
    # Assert
    # -------------------------

    assert (output_dir / "index.md").exists()
    assert (output_dir / "UserTest.md").exists()

    user_test_contents = (output_dir / "UserTest.md").read_text()

    print(user_test_contents)

    assert "# UserTest" in user_test_contents
    assert "## LoginTests" in user_test_contents
    assert "## Test Methods" in user_test_contents
    assert "- Method: `shouldCreateUser`" in user_test_contents
    assert "## Dependencies" in user_test_contents
    assert "```mermaid" in user_test_contents

    assert (output_dir / "UserRepositoryTest.md").exists()
    assert (output_dir / "OrderTest.md").exists()

    order_test_contents = (output_dir / "OrderTest.md").read_text()

    assert "# OrderTest" in order_test_contents
    assert "## Summary" in user_test_contents
    assert "- Tests: 1"
    
    assert (output_dir / "dependency_graph.md").exists()

    