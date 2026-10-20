import urllib.request
import re
import json

video_id = "C2uF4vNZLkU"
url = f"https://www.youtube.com/watch?v={video_id}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});var", html)
if not player_match:
    player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});", html)

if player_match:
    player_data = json.loads(player_match.group(1))
    video_details = player_data.get("videoDetails", {})
    title = video_details.get("title")
    author = video_details.get("author")
    desc = video_details.get("shortDescription")
    
    with open("scratch/video_info.json", "w", encoding="utf-8") as f:
        json.dump({"title": title, "author": author, "description": desc}, f, ensure_ascii=False, indent=2)
        
    captions = player_data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
    if captions:
        track = captions[0]
        track_url = track.get("baseUrl")
        print("Track URL:", track_url)
        # Fetch as json3 or srv3
        if track_url:
            with urllib.request.urlopen(track_url) as cap_resp:
                raw_cap = cap_resp.read().decode("utf-8", errors="ignore")
                with open("scratch/raw_caption.xml", "w", encoding="utf-8") as f:
                    f.write(raw_cap)
            
            # Also try fmt=json3
            json3_url = track_url + "&fmt=json3"
            try:
                with urllib.request.urlopen(json3_url) as j_resp:
                    raw_j = j_resp.read().decode("utf-8", errors="ignore")
                    with open("scratch/caption.json", "w", encoding="utf-8") as f:
                        f.write(raw_j)
            except Exception as e:
                print("json3 error:", e)
