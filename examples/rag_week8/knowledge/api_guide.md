# api_guide.md

# Product Normalizer API Guide

The product-normalizer project exposes several FastAPI endpoints.

## GET /health

Checks whether the API service is running.

Example response:

{
  "status": "ok"
}

## POST /normalize

Uploads UPC and product Excel files.

The system validates, cleans, merges, and standardizes the data.

The response is a standardized Excel file.

## GET /runs

Returns recent processing runs stored in SQLite.

It can be used to view processing history.

## GET /runs/{run_id}

Returns details for one processing run.

The response may include:

- status
- input row counts
- output row count
- validation issue count
- start time
- finish time

## GET /runs/{run_id}/issues

Returns validation issues belonging to a specific processing run.

## POST /generate-listing

Uses an LLM to generate structured e-commerce listing content.

The input contains product information such as:

- SKU
- title
- color
- category
- price

The output contains:

- SKU
- listing title
- bullet points
- description

## POST /assistant

Accepts a natural-language message.

The LLM can decide whether it needs to call a tool.

Available tools include:

- get_runs
- get_run_detail
- get_run_issues

The assistant can use real database results before producing the final answer.