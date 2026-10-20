from youtube_transcript_api import YouTubeTranscriptApi
import json

video_id = "C2uF4vNZLkU"

try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    print("Available transcripts:")
    for t in transcript_list:
        print(f" - {t.language} ({t.language_code}), generated: {t.is_generated}")
    
    # Try fetching korean transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
    full_text = "\n".join([f"[{item['start']:.1f}s] {item['text']}" for item in transcript])
    print("Transcript fetched successfully! Length:", len(full_text))
    
    with open("scratch/transcript_with_timestamps.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    plain_text = " ".join([item['text'] for item in transcript])
    with open("scratch/full_transcript.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)
        
    print("Saved to scratch/full_transcript.txt and scratch/transcript_with_timestamps.txt")
except Exception as e:
    print("Error getting transcript:", e)
