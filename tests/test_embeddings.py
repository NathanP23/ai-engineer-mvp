# we need the chunking module to test its pure, file-free splitting logic
from src.embeddings import chunk_documents

# we need the embedding module to test its pure, model-free attachment logic
from src.embeddings import embed_chunks


# this test checks that a short text shorter than the chunk size becomes exactly one chunk
def test_chunk_text_returns_single_chunk_for_short_text() -> None:
    # this calls the function under test with a chunk size much bigger than the text
    chunks = chunk_documents.chunk_text("hello world", chunk_size=800, overlap=150)
    # this checks the whole short text came back as one single chunk
    assert chunks == ["hello world"]


# this test checks that a long text gets split into multiple chunks with real overlap between them
def test_chunk_text_splits_long_text_with_overlap() -> None:
    # this builds a text of exactly 30 characters, all distinct so overlap is easy to verify
    text = "".join(str(digit % 10) for digit in range(30))
    # this calls the function under test with a small chunk size so we get several chunks
    chunks = chunk_documents.chunk_text(text, chunk_size=10, overlap=3)
    # this checks we got more than one chunk out of a text longer than the chunk size
    assert len(chunks) > 1
    # this checks the end of the first chunk really does reappear at the start of the second
    assert chunks[0][-3:] == chunks[1][:3]


# this test checks that whitespace-only slices at the end of a text don't become empty chunks
def test_chunk_text_skips_whitespace_only_trailing_chunk() -> None:
    # this text is exactly one chunk of real content followed by only whitespace
    text = "a" * 10 + "   "
    # this calls the function under test with a chunk size that would otherwise produce a blank tail chunk
    chunks = chunk_documents.chunk_text(text, chunk_size=10, overlap=0)
    # this checks every returned chunk has real, non-whitespace content
    assert all(chunk.strip() for chunk in chunks)


# this test checks that build_chunk_records attaches the right doc_slug and chunk_index to each piece
def test_build_chunk_records_attaches_metadata() -> None:
    # this calls the function under test with a short doc that chunk_text will keep as one piece
    records = chunk_documents.build_chunk_records("mqtt", "a short mqtt doc")
    # this checks exactly one record came back, with the expected metadata and text
    assert records == [{"doc_slug": "mqtt", "chunk_index": 0, "text": "a short mqtt doc"}]


# this test checks that attach_embeddings adds an "embedding" field using whatever function it's given
def test_attach_embeddings_adds_embedding_field() -> None:
    # these are two fake chunk records, shaped like what chunk_documents.py would produce
    chunk_records = [
        {"doc_slug": "mqtt", "chunk_index": 0, "text": "hello"},
        {"doc_slug": "mqtt", "chunk_index": 1, "text": "world!"},
    ]
    # this is a fake, deterministic "embedding function" so the test never loads a real model
    fake_embed_fn = lambda text: [len(text)]
    # this calls the function under test with our fake embedding function
    embedded_records = embed_chunks.attach_embeddings(chunk_records, fake_embed_fn)
    # this checks every original field survived, plus the new embedding computed by our fake function
    assert embedded_records == [
        {"doc_slug": "mqtt", "chunk_index": 0, "text": "hello", "embedding": [5]},
        {"doc_slug": "mqtt", "chunk_index": 1, "text": "world!", "embedding": [6]},
    ]
