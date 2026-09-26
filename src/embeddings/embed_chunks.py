# we need json to read the chunked documents and write the embedded ones back out
import json

# we need this class to load a real sentence-embedding model
from sentence_transformers import SentenceTransformer

# we need our shared settings so the embedding model name and file paths all live in one place
from src.config import settings


# this function reads the chunk records that chunk_documents.py already wrote to disk
def load_chunks() -> list[dict]:
    # this reads the whole chunks file and parses it back into a list of dicts
    return json.loads(settings.CHUNKS_OUTPUT_PATH.read_text())


# this function downloads (or loads from cache) the real sentence-embedding model
def load_embedding_model(model_name: str) -> SentenceTransformer:
    # this constructs the model, ready to turn text into vectors
    return SentenceTransformer(model_name)


# this function attaches an embedding vector to every chunk record, using whatever embed_fn is given
def attach_embeddings(chunk_records: list[dict], embed_fn) -> list[dict]:
    # this will collect a new list of records so we don't mutate the input in place
    embedded_records = []
    # walk through every chunk record one at a time
    for record in chunk_records:
        # this computes the embedding vector for just this chunk's text
        embedding = embed_fn(record["text"])
        # this builds a new record that has every original field plus the new embedding
        embedded_records.append({**record, "embedding": embedding})
    # hand back every record, now carrying its embedding vector
    return embedded_records


# this function writes the embedded chunk records out to disk as a single JSON file
def save_embedded_chunks(embedded_records: list[dict]) -> None:
    # this makes sure the processed-data folder exists before we try to write into it
    settings.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    # this writes every embedded record out as one pretty-printed JSON array
    settings.EMBEDDED_CHUNKS_OUTPUT_PATH.write_text(json.dumps(embedded_records, indent=2))


# this is the entry point used when this script is run directly
def main() -> None:
    # this reads the chunk records produced by chunk_documents.py
    chunk_records = load_chunks()
    # this loads the real embedding model we'll use to compute every vector
    model = load_embedding_model(settings.EMBEDDING_MODEL_NAME)
    # this wraps the model's encode call so attach_embeddings never needs to know about the model directly
    embed_fn = lambda text: model.encode(text).tolist()
    # this computes and attaches an embedding vector to every chunk record
    embedded_records = attach_embeddings(chunk_records, embed_fn)
    # this saves every embedded record to disk for Stage 4 (Qdrant) to read
    save_embedded_chunks(embedded_records)
    # this reports how many chunks were embedded and how long each vector is
    embedding_dimension = len(embedded_records[0]["embedding"]) if embedded_records else 0
    # this prints a friendly summary of the whole run
    print(f"embedded {len(embedded_records)} chunks (dimension {embedding_dimension}) to {settings.EMBEDDED_CHUNKS_OUTPUT_PATH}")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off embedding
    main()
