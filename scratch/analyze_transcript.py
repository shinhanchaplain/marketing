import re
import json

with open("scratch/full_transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

with open("scratch/transcript_with_timestamps.txt", "r", encoding="utf-8") as f:
    timestamps = f.readlines()

print(f"Total characters: {len(text)}")
print(f"Total lines with timestamps: {len(timestamps)}")

# Let's search for key terms
keywords = [
    "상세페이지", "스마트스토어", "기획", "후킹", "소구점", "문제", "해결",
    "리뷰", "경쟁사", "옵션", "가격", "설득", "신뢰", "후기",
    "1단계", "2단계", "3단계", "4단계", "5단계", "구조", "프레임워크",
    "프롬프트", "chatgpt", "gpt", "ai", "클로드", "claude",
    "인트로", "바디", "아웃트로", "구매전환", "상세", "키워드"
]

keyword_counts = {}
for kw in keywords:
    matches = len(re.findall(re.escape(kw), text, re.IGNORECASE))
    if matches > 0:
        keyword_counts[kw] = matches

print("Keyword counts:", json.dumps(keyword_counts, ensure_ascii=False, indent=2))

# Find sections where AI or frameworks are explained
chunks = []
chunk_size = 3000
for i in range(0, len(text), chunk_size):
    chunk = text[i:i+chunk_size]
    chunks.append({
        "index": i // chunk_size,
        "sample": chunk[:200]
    })

print(f"Total chunks ({chunk_size} chars each): {len(chunks)}")
