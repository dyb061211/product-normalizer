from langchain_huggingface import HuggingFaceEmbeddings

embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
)

texts = [
    "Maximum tool rounds is 3.",
    "The agent allows three tool calls before stopping.",
    "Portable camping chair costs 29.99 dollars."
]
vectors=embeddings.embed_documents(texts)
print(type(vectors))
print(len(vectors))
print(type(vectors[0]))
print(len(vectors[0]))
for vector in vectors:
    print(vector[:5])