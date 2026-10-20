from youtube_transcript_api import YouTubeTranscriptApi

video_id = "C2uF4vNZLkU"

api = YouTubeTranscriptApi()
tl = api.list(video_id)
print("Transcript list available:")
for t in tl:
    print(f" - {t.language} ({t.language_code}) generated={t.is_generated}")

# Find ko or fallback
t = tl.find_transcript(['ko'])
fetched = t.fetch()
print("Total caption entries:", len(fetched))

lines = []
for item in fetched:
    # item may be an object or dict
    if hasattr(item, 'text'):
        text = item.text
        start = item.start
    else:
        text = item['text']
        start = item['start']
    lines.append(f"[{start:.1f}s] {text}")

full_text = "\n".join(lines)
with open("scratch/transcript_with_timestamps.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

plain_lines = []
for item in fetched:
    if hasattr(item, 'text'):
        plain_lines.append(item.text)
    else:
        plain_lines.append(item['text'])

with open("scratch/full_transcript.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(plain_lines))

print("Successfully written to scratch/transcript_with_timestamps.txt and scratch/full_transcript.txt!")
