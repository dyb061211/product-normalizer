from pathlib import Path
from langchain_core.documents import Document

def load_documents(knowledge_dir:Path)->list[Document]:
    if not knowledge_dir.exists():
        raise FileNotFoundError(f"knowledge directory does not exist: {knowledge_dir}")
    documents=[]
    md_files=list(knowledge_dir.glob("*.md"))
    if not md_files:
        raise ValueError(f"no md files in {knowledge_dir}")
    for file_path in md_files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError,UnicodeDecodeError) as exc:
            raise OSError(
                f"failed to read knowledge file: {file_path}"
            ) from exc
        document=Document(
            page_content=content,
            metadata={
                "source":str(file_path),
                "filename":file_path.name
            }
        )
        documents.append(document)
    return documents


