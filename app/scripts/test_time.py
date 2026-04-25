#measure chunk_text for a 100 page pdf
from app.tasks.processing.chunk_text import chunk_text
import time
with open('E:\\Coding\\Gnosis\\app\\scripts\\filename.txt', 'r',encoding='utf-8') as file:
    text = file.read()

start=time.time()
chunks = chunk_text(text=text)
print(chunks)
print(f"Total chunks: {len(chunks)}")

# Print last chunk only
print("\nLAST CHUNK:\n")
print(chunks[-1])

# Check if end of original text is present
print("\nEND OF ORIGINAL TEXT:\n")
print(text[-500:])

end=time.time()

print(f"{end-start} was the time taken for this function to chunk 260 paage document")
