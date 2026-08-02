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

---

## Example Output

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

\`\`\`mermaid
UserTest --> User
UserTest --> UserRepository
\`\`\`

## Test Methods:

### Users can be created

- Method: \`shouldCreateUser\`
- Tags: user, unit
- Disabled: No
- Source: UserTest.java:25



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

The project index provides an overview of the test suite, including:

- Total packages
- Test files
- Test classes
- Test methods
- Disabled tests
- Package organization

### \<TestClass\>.md

Each generated test class document contains:

- Class information
- Package
- Sumamry statistics
- Dependencies
- Mermaid dependency graph
- Test methods
- Source location

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
Dependency Analyzer
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

- **Coverage reports**, mapping production classes to the tests that reference them.
- **Callouts** for parametrized tests, lifeclyle methods, and repeated tests.
- **Configuration support** (ingnoe packages, customize output paths, include/exclude sections).
- **Cross-linking** between generated Markdown pages
- **Package-level dependency graphs** in addition to per-class graphs.
