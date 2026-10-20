from youtube_transcript_api import YouTubeTranscriptApi

video_id = "C2uF4vNZLkU"

try:
    # Try list
    tl = YouTubeTranscriptApi.list(video_id)
    print("Found transcripts:")
    t_obj = tl.find_transcript(['ko'])
    fetched = t_obj.fetch()
    print("Fetched items:", len(fetched))
    
    full_text = "\n".join([f"[{item['start']:.1f}s] {item['text']}" for item in fetched])
    with open("scratch/transcript_with_timestamps.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    plain_text = " ".join([item['text'] for item in fetched])
    with open("scratch/full_transcript.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)
        
    print("SUCCESS! Saved transcript.")
except Exception as e:
    print("Error:", e)
    # try fetch directly
    try:
        f = YouTubeTranscriptApi.fetch(video_id)
        print("Fetched directly:", len(f))
    except Exception as e2:
        print("Fetch directly error:", e2)
