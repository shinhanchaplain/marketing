import urllib.request
import re
import json

video_id = "C2uF4vNZLkU"
url = f"https://www.youtube.com/watch?v={video_id}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    
    title_match = re.search(r"<title>(.*?)</title>", html)
    print("TITLE:", title_match.group(1) if title_match else "Unknown")
    
    # Try finding ytInitialPlayerResponse
    player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});var", html)
    if not player_match:
        player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});", html)
        
    if player_match:
        player_data = json.loads(player_match.group(1))
        video_details = player_data.get("videoDetails", {})
        print("VIDEO TITLE:", video_details.get("title"))
        print("AUTHOR:", video_details.get("author"))
        print("SHORT DESC:\n", video_details.get("shortDescription", "")[:1000])
        
        # Check captions
        captions = player_data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
        print("CAPTION TRACKS:", len(captions))
        for track in captions:
            print("Track:", track.get("languageCode"), track.get("name", {}).get("simpleText"))
            track_url = track.get("baseUrl")
            if track_url:
                with urllib.request.urlopen(track_url) as cap_resp:
                    cap_xml = cap_resp.read().decode("utf-8", errors="ignore")
                    text_lines = re.findall(r"<text[^>]*>(.*?)</text>", cap_xml)
                    clean_text = " ".join([re.sub(r"&[a-z]+;", " ", t) for t in text_lines])
                    print(f"CAPTION SAMPLE ({track.get('languageCode')}):", clean_text[:2000])
                    with open(f"scratch/caption_{track.get('languageCode')}.txt", "w", encoding="utf-8") as f_out:
                        f_out.write(clean_text)
    else:
        print("Could not find ytInitialPlayerResponse")
except Exception as e:
    print("Error:", e)
