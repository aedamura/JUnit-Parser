# JUnit Test Parser

JUnit Test Indexer is a static analysis tool that scans JUnit 5 test suites and
generates Markdown documentation for individual test classes and the project as
a whole. It extracts test metadata, identifies dependencies, and produces
Mermaid diagrams to make large test suites easier to navigate and understand.

---

## Features

- Parses JUnit 5 test classes
- Detects nested test classes
- Extracts annotations, tags, and source locations
- Generates Markdown documentation
- Produces Mermaid dependency graphs
- Generates project-wide documentation index
- Provides project-wide metrics
- Generates a coverage report
- Cross-links between generated files

---

## Example Output

### index.md

```markdown
# JUnit Test Documentation

## Project Summary
- Packages: 7
- Test Files: 14
- Test Classes: 52
- Nested Classes: 38
- Test Methods: 152
- Parameterized Tests: 27
- Disabled Tests: 0
- Tagged Tests: 151
- Lifecycle Methods: 9

---

## Packages

### `com.example.users`

- UserTest
    - LoginTest
...

---

## Dependency Graph

(Rendered Mermaid Graph)

```

### \<Test Class\>.md

```markdown
# UserTest

## Package

com.example.users

## Summary

- Tests: 5
- Disabled: 0
- Tagged: 3

## Dependencies

### List:

- com.example.users.User
- com.example.repositories.UserRepository

### Graph:

\```mermaid
graph TD
UserTest --> User
UserTest --> UserRepository
\```

## Test Methods:

### Users can be created

- Method: \`shouldCreateUser\`
- Tags: user, unit
- Disabled: No
- Source: UserTest.java:25



```

### coverage_report.md

```markdown
# Coverage Report

## Coverage

### com.example.users.User

- com.example.users.UserTest
- com.example.orders.OrderTest

...

```

---

## Installation

`pip install -r requirements.txt`

---

## Usage

`python main.py <source-directory> <output-directory>`

Example:
`python main.py ./src/test/java ./docs`

---

## Generated Documentation

The generated documentation consists of one Markdown file for each test class,
along with a project-wide index.

### index.md

The project index provides an overview of the entrire test suite, including:

- Total packages
- Test files
- Test classes
- Test methods
- Disabled tests
- Package organization
- Project-wide dependency graph

See [example output](#indexmd).

### \<TestClass\>.md

Each generated test class document contains:

- Class information
- Package
- Summary statistics
- Dependencies
- Mermaid dependency graph
- Test methods
- Source location

See [example output](#test-classmd).

### coverage_report.md

The coverage report displays which production classes are exercised by which test classes.
The report is generated as a list. See [example output](#coverage_reportmd).

---

## Project Architecture

Scanner
↓
Parser
↓
JUnit Analyzer
↓
Indexer
↓
Project Analyzer
↓
Dependency Analyzer
↓
Coverage Analyzer
↓
Documentation Generator
↓
Markdown Generator

---

## Limitations

Supports:

- JUnit 5
- Nested tests

Does not yet support:

- Wildcard imports
- Static imports
- Full production source parsing

---

## Roadmap

- **Callouts** for parametrized tests, lifeclyle methods, and repeated tests.
- **Configuration support** (ingnoe packages, customize output paths, include/exclude sections).
- **Better Parser Support** for wildcard and static imports, generic types
- **Package-level dependency graphs** in addition to per-class graphs.
