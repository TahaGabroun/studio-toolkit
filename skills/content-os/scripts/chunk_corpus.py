"""Index a licensed Markdown corpus into overlapping SQLite chunks.

Usage: python chunk_corpus.py SOURCE_DIRECTORY DATABASE
Adapted from Content OS; see LICENSE.upstream.txt and SOURCES.md.
"""

import sqlite3
import re
from pathlib import Path
from typing import Iterator

# Configuration
SOURCE_DIR = Path(".")
OUTPUT_DB = Path("corpus.db")
CHUNK_SIZE = 150  # words per chunk (smaller = denser content gets own chunk)
OVERLAP = 25      # word overlap between chunks


def extract_metadata(filename: str) -> dict:
    """Extract optional sequence and year from a structured Markdown filename."""
    # Pattern: sequence_title_year.md
    match = re.match(r'(\d+)_.*?(\d{4})\.md$', filename)
    if match:
        sequence = int(match.group(1))
        year = int(match.group(2))
        return {
            'sequence': sequence,
            'year': year,
            'filename': filename,
        }
    return {'sequence': 0, 'year': 0, 'filename': filename}


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> Iterator[tuple[str, int]]:
    """
    Split text into overlapping chunks of approximately chunk_size words.
    Yields (chunk_text, start_position).
    """
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require 0 <= overlap < chunk_size")
    # Clean up the text
    text = re.sub(r'\n{3,}', '\n\n', text)  # Normalize multiple newlines
    text = re.sub(r'---+', '', text)         # Remove markdown separators

    words = text.split()
    if not words:
        return

    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)

        # Only yield if chunk has substantial content
        if len(chunk_text.strip()) > 50:
            yield chunk_text, start

        # Move forward, accounting for overlap
        start = start + chunk_size - overlap
        if start >= len(words):
            break


def create_database(db_path: Path):
    """Create the SQLite database schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT UNIQUE,
            title TEXT,
            sequence INTEGER,
            year INTEGER,
            word_count INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            document_id INTEGER,
            content TEXT,
            word_position INTEGER,
            chunk_index INTEGER,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    ''')

    conn.commit()
    return conn


def process_essays(source_dir: Path, conn: sqlite3.Connection):
    """Process all markdown files and chunk them into the database."""
    cursor = conn.cursor()

    md_files = sorted(source_dir.glob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    total_chunks = 0

    for md_file in md_files:
        # Skip composite file
        if 'composite' in md_file.name.lower():
            print(f"  Skipping composite: {md_file.name}")
            continue

        print(f"  Processing: {md_file.name}")

        # Read content
        content = md_file.read_text(encoding='utf-8', errors='ignore')
        words = content.split()

        # Extract metadata
        meta = extract_metadata(md_file.name)
        title = md_file.stem

        # Insert document
        cursor.execute('''
            INSERT OR IGNORE INTO documents (filename, title, sequence, year, word_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (md_file.name, title, meta['sequence'], meta['year'], len(words)))

        doc_id = cursor.execute("SELECT id FROM documents WHERE filename=?", (md_file.name,)).fetchone()[0]
        cursor.execute("DELETE FROM chunks WHERE document_id=?", (doc_id,))

        # Chunk and insert
        chunk_idx = 0
        for chunk_text, word_pos in split_into_chunks(content):
            cursor.execute('''
                INSERT INTO chunks (document_id, content, word_position, chunk_index)
                VALUES (?, ?, ?, ?)
            ''', (doc_id, chunk_text, word_pos, chunk_idx))
            chunk_idx += 1
            total_chunks += 1

        print(f"    -> {chunk_idx} chunks, {len(words)} words")

    conn.commit()
    print(f"\nTotal: {total_chunks} chunks from {len(md_files)} documents")
    return total_chunks


def main():
    import argparse
    global SOURCE_DIR, OUTPUT_DB
    parser = argparse.ArgumentParser(description="Index a licensed Markdown corpus into SQLite chunks")
    parser.add_argument("source", type=Path)
    parser.add_argument("database", type=Path)
    a = parser.parse_args()
    SOURCE_DIR, OUTPUT_DB = a.source, a.database
    print("Studio corpus chunker")
    print("=" * 40)

    # Check source directory
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        print("Make sure you run this from the scripts/ directory")
        return

    # Create database
    print(f"\nCreating database: {OUTPUT_DB}")
    conn = create_database(OUTPUT_DB)

    # Process essays
    print(f"\nChunking essays from: {SOURCE_DIR}")
    total = process_essays(SOURCE_DIR, conn)

    # Summary
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM chunks")
    chunk_count = cursor.fetchone()[0]

    print(f"\n{'=' * 40}")
    print("DATABASE READY")
    print(f"{'=' * 40}")
    print(f"Documents: {doc_count}")
    print(f"Chunks: {chunk_count}")
    print(f"Database: {OUTPUT_DB}")

    conn.close()


if __name__ == "__main__":
    main()
