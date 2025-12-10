import re
import json
from pathlib import Path


def clean_gutenberg_text(text):
    """Remove Project Gutenberg header and footer."""
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
        "*END*THE SMALL PRINT"
    ]
    
    start_idx = 0
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            start_idx = text.find('\n', idx) + 1
            break
    
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
        "End of the Project Gutenberg"
    ]
    
    end_idx = len(text)
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_idx = idx
            break
    
    return text[start_idx:end_idx].strip()


def parse_by_paragraphs(text):
    """Split text into paragraphs (separated by blank lines)."""
    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def parse_by_sentences(text):
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def parse_by_chunks(text, chunk_size=512, overlap=50):
    """Split text into fixed-size chunks with optional overlap."""
    chunks = []
    start = 0
    text = text.strip()
    
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks


def parse_by_lines(text):
    """Split text into lines, removing empty lines."""
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def load_and_process_textbook(
    filepath,
    method='paragraphs',
    chunk_size=512,
    overlap=50,
    clean=True
):
    """
    Load and process a textbook file into a list of strings.
    
    Args:
        filepath: Path to the .txt file
        method: 'paragraphs', 'sentences', 'chunks', or 'lines'
        chunk_size: Size of chunks if method='chunks'
        overlap: Overlap size if method='chunks'
        clean: Whether to remove Gutenberg headers/footers
    
    Returns:
        list: List of text strings
    """
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean if requested
    if clean:
        text = clean_gutenberg_text(text)
    
    # Parse based on method
    if method == 'paragraphs':
        return parse_by_paragraphs(text)
    elif method == 'sentences':
        return parse_by_sentences(text)
    elif method == 'chunks':
        return parse_by_chunks(text, chunk_size, overlap)
    elif method == 'lines':
        return parse_by_lines(text)
    else:
        raise ValueError(f"Unknown method: {method}")


def save_processed_data(text_list, output_path, format='json'):
    """
    Save processed text list to file.
    
    Args:
        text_list: List of strings to save
        output_path: Path to output file
        format: 'json', 'txt', or 'pickle'
    """
    output_path = Path(output_path)
    
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(text_list, f, indent=2, ensure_ascii=False)
    elif format == 'txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in text_list:
                f.write(item + '\n---\n')
    elif format == 'pickle':
        import pickle
        with open(output_path, 'wb') as f:
            pickle.dump(text_list, f)
    else:
        raise ValueError(f"Unknown format: {format}")


def load_processed_data(input_path, format='json'):
    """
    Load processed text list from file.
    
    Args:
        input_path: Path to input file
        format: 'json', 'txt', or 'pickle'
    
    Returns:
        list: List of text strings
    """
    input_path = Path(input_path)
    
    if format == 'json':
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif format == 'txt':
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return [item.strip() for item in content.split('---') if item.strip()]
    elif format == 'pickle':
        import pickle
        with open(input_path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unknown format: {format}")
    

def load_and_process_multiple_files(
    file_paths,
    num_files=None,
    method='paragraphs',
    chunk_size=512,
    overlap=50,
    preserve_chapter_boundaries=False
):
    """Process multiple chapter files
    Args: 
        file_paths: list of paths to markdown files
        num_files: optional count of files to process (default all)
        preserve_chapter_boundaries: bool for adding chapter metadata
    """
    all_segments = []

    selected_paths = file_paths if num_files is None else file_paths[:num_files]

    for i, file_path in enumerate(selected_paths):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Process the chapter
        if method == 'paragraphs':
            segments = parse_by_paragraphs(text)
        elif method == 'sentences':
            segments = parse_by_sentences(text)
        elif method == 'chunks':
            segments = parse_by_chunks(text, chunk_size, overlap)
        elif method == 'lines':
            segments = parse_by_lines(text)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if preserve_chapter_boundaries:
            segments = [{'chapter': i+1, 'text':seg} for seg in segments]

        all_segments.extend(segments)

    return all_segments


if __name__ == "__main__":
    base_chapter_dir = Path('sae_core/data/raw_data')
    subject_folders = {
        'physics': 'physics_chapters',
        'chemistry': 'chemistry_chapters',
        'biology': 'biology_chapters'
    }
    output_path = Path('sae_core/data/processed_data/processed_textbooks_all.json')

    # Shared processing options
    method = 'paragraphs'
    chunk_size = 512
    overlap = 50
    preserve_chapter_boundaries = False

    combined_segments = []

    for subject, folder_name in subject_folders.items():
        chapter_dir = base_chapter_dir / folder_name
        chapter_files = sorted(chapter_dir.glob('*.md'))

        if not chapter_files:
            raise FileNotFoundError(f"No .md files found in {chapter_dir}")

        print(f"[{subject}] Found {len(chapter_files)} chapter files")

        subject_segments = load_and_process_multiple_files(
            chapter_files,
            num_files=None,
            method=method,
            chunk_size=chunk_size,
            overlap=overlap,
            preserve_chapter_boundaries=preserve_chapter_boundaries
        )

        print(f"[{subject}] Processed {len(subject_segments)} text segments")
        combined_segments.extend(subject_segments)

    print(f"Total segments combined: {len(combined_segments)}")
    if combined_segments:
        sample_entry = combined_segments[0]
        preview = sample_entry if isinstance(sample_entry, str) else sample_entry.get('text', '')
        print(f"Sample segment: {preview[:200]}...")

    save_processed_data(combined_segments, output_path)
    print(f"Saved combined dataset to {output_path}")
