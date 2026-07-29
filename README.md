# JUnit-Parser

JUnit Parser is a tool for automatically generating documentation for the project's JUnit test suite.

## Features

- Index every test class
- Parse JUnit 5 annotations
- Generate Markdown documentation
- Generate dependency graphs
- Produce feature coverage reports

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

JUnit Parser/
    analyzer.py
    annotations.py
    indexer.py
    models.py
    parser.py
    scanner.py