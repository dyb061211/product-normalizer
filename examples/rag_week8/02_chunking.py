from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

doucment=Document(
    page_content="""
    product normalizer handles product data cleaning validation merging standardization api requests tool calling error handling database history listing generation assistant requests and project processing
    """
)

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10
)

chunks=text_splitter.split_documents(
    [doucment]
)

print(type(chunks))
print(len(chunks))

for i,chunk in enumerate(chunks):
    print("chunk:",i)
    print(type(chunk))
    print(chunk.page_content)
    print("length:",len(chunk.page_content))
    print()