def split_text(text:str, chunk_size: int = 500) -> list[str]:
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)
            

    return chunks