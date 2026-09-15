# project_overview.md

# Product Normalizer Project Overview

product-normalizer is a Python project for cleaning, validating, merging, and standardizing e-commerce product data.

The project mainly works with Excel files containing product information such as SKU, UPC, title, price, stock, color, and category.

## Main Modules

- reader.py: reads Excel files
- mapper.py: standardizes column names
- validator.py: validates required fields and detects data issues
- cleaner.py: normalizes and cleans product data
- merger.py: merges UPC data with product data
- exporter.py: exports standardized results and validation reports
- service.py: coordinates the complete product processing workflow
- repository.py: reads and writes processing history in SQLite
- database.py: manages SQLite database connections

## Week 1

The project was first divided into multiple Python modules.

The main workflow became:

Excel files
→ read
→ standardize columns
→ clean data
→ merge data
→ export standardized Excel

## Week 2

The project added engineering reliability features:

- custom exceptions
- logging
- validation
- pytest
- Git and GitHub

## Week 3

FastAPI was added.

The project can receive uploaded Excel files through HTTP and return a standardized Excel file.

## Week 4

SQLite persistence was added.

The system stores processing history in:

- processing_runs
- validation_issues

The repository layer is responsible for database access.