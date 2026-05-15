from typing import List

#overlap
# ASIS: A B C D E F G H I J

#chunk 0: A B C D E
#chunk 1: F G H I J
# -> E와 F 사이의 문맥이 끊김

# chunk 0: A B C D E
# chunk 1: D E F G H
# chunk 2: G H I J
# -> 문맥 유지

def split_text_into_chunks(
    text: str,
    chunk_size: int=800,
    chunk_overlap: int=100
) -> List[str]:
    if not text:
        return []
    
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap은 chunk_size보다 작아야 합니다.")
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)
        
        start = end - chunk_overlap

        if start >= text_length:
            break
    
    return chunks


