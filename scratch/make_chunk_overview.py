with open("scratch/full_transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunk_size = 3000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

with open("scratch/chunk_overview.txt", "w", encoding="utf-8") as f:
    for idx, c in enumerate(chunks):
        f.write(f"=== CHUNK {idx} (Length: {len(c)}) ===\n")
        f.write(c[:500] + "\n...\n\n")

print(f"Wrote {len(chunks)} chunks overview.")
