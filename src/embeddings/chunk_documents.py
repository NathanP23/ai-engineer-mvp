# we need json to write the chunked documents out to disk
import json

# we need our shared settings so chunk size, overlap, and file paths all live in one place
from src.config import settings


# ponytail: a character-based sliding window, not a sentence/token-aware splitter — it can cut
# a sentence in half at a chunk boundary. Upgrade to a sentence-boundary-aware splitter if
# retrieval quality (Stage 4) turns out to suffer from awkward mid-sentence cuts.
# this function splits one document's text into overlapping, fixed-size character chunks
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    # this will collect every chunk we cut from this document
    chunks = []
    # this tracks where the next chunk should start reading from
    start_index = 0
    # keep cutting chunks until we've covered the whole document
    while start_index < len(text):
        # this is where the current chunk should stop reading
        end_index = start_index + chunk_size
        # this is the actual slice of text for the current chunk
        chunk = text[start_index:end_index]
        # only keep the chunk if it has real content, not just trailing whitespace
        if chunk.strip():
            # add this chunk to the list we're building up
            chunks.append(chunk)
        # this moves the start forward, but re-reads the last `overlap` characters of this chunk
        start_index += chunk_size - overlap
    # hand back every chunk we cut from this document
    return chunks


# this function reads every real markdown doc fetched in Stage 1 into memory
def load_raw_docs() -> dict[str, str]:
    # this will map each integration's slug to its full document text
    docs_by_slug = {}
    # walk through every markdown file that Stage 1 actually saved
    for doc_path in sorted(settings.DOCS_OUTPUT_DIR.glob("*.md")):
        # the file's name without its extension is the integration's slug
        slug = doc_path.stem
        # this reads the full text of one document
        docs_by_slug[slug] = doc_path.read_text()
    # hand back every document we found, keyed by slug
    return docs_by_slug


# this function turns one document's full text into a list of chunk records with metadata attached
def build_chunk_records(doc_slug: str, doc_text: str) -> list[dict]:
    # this cuts the document into overlapping character chunks using our configured sizes
    raw_chunks = chunk_text(doc_text, settings.CHUNK_SIZE_CHARS, settings.CHUNK_OVERLAP_CHARS)
    # this will collect one record per chunk, each carrying the metadata retrieval will need later
    records = []
    # walk through every chunk, keeping track of its position within this document
    for chunk_index, chunk in enumerate(raw_chunks):
        # build a record that remembers which document and position this chunk came from
        records.append({
            "doc_slug": doc_slug,
            "chunk_index": chunk_index,
            "text": chunk,
        })
    # hand back every chunk record for this one document
    return records


# this function writes every chunk record from every document out to a single JSON file
def save_chunks(all_chunk_records: list[dict]) -> None:
    # this makes sure the processed-data folder exists before we try to write into it
    settings.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    # this writes every chunk record out as one pretty-printed JSON array
    settings.CHUNKS_OUTPUT_PATH.write_text(json.dumps(all_chunk_records, indent=2))


# this is the entry point used when this script is run directly
def main() -> None:
    # this loads every real document Stage 1 fetched, keyed by integration slug
    docs_by_slug = load_raw_docs()
    # this will collect chunk records from every document into one flat list
    all_chunk_records = []
    # walk through every document one at a time
    for doc_slug, doc_text in docs_by_slug.items():
        # this cuts the current document into chunk records with metadata attached
        chunk_records = build_chunk_records(doc_slug, doc_text)
        # this adds the current document's chunks into the overall flat list
        all_chunk_records.extend(chunk_records)
        # this reports progress for the current document as chunking proceeds
        print(f"chunked '{doc_slug}' into {len(chunk_records)} chunk(s)")
    # this saves every chunk from every document into one JSON file for the next stage to read
    save_chunks(all_chunk_records)
    # this prints a final summary of the whole run
    print(f"saved {len(all_chunk_records)} total chunks to {settings.CHUNKS_OUTPUT_PATH}")


# this block only runs main() when the file is executed directly, not when it's imported
if __name__ == "__main__":
    # this actually calls main() to kick off chunking
    main()
