from langchain_core.documents import Document

document1=Document(
    page_content="MAX_TOOL_ROUNDS is 3",
    metadata={
        "source":"error_handling.md",
        "topic":"agent"
    }
)

document2=Document(
    page_content="product-normalizer is a Python project for cleaning, validating, merging, and standardizing e-commerce product data.",
    metadata={
        "source":"project_overview.md"
    }
)

document3=Document(
    page_content="The product-normalizer project exposes several FastAPI endpoints.",
    metadata={
        "source":"api_guide.md"
    }
)

documents=[document1,document2,document3]
print(type(documents))
print(type(documents[0]))