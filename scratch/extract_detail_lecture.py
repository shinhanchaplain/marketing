with open("scratch/full_transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunks 0 to 4 comprise the first 15,000 characters
detail_page_lecture = text[:15000]

with open("scratch/detail_page_lecture.txt", "w", encoding="utf-8") as f:
    f.write(detail_page_lecture)

print("Saved detail_page_lecture.txt (first 15,000 chars)")
