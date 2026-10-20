import json
import xml.etree.ElementTree as ET
import html
import os

# Try json first
transcript_text = []

if os.path.exists("scratch/caption.json") and os.path.getsize("scratch/caption.json") > 0:
    try:
        with open("scratch/caption.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            events = data.get("events", [])
            for ev in events:
                segs = ev.get("segs", [])
                line = "".join([s.get("utf8", "") for s in segs]).strip()
                if line:
                    transcript_text.append(line)
    except Exception as e:
        print("JSON parse error:", e)

if not transcript_text and os.path.exists("scratch/raw_caption.xml") and os.path.getsize("scratch/raw_caption.xml") > 0:
    try:
        with open("scratch/raw_caption.xml", "r", encoding="utf-8") as f:
            raw_xml = f.read()
        root = ET.fromstring(raw_xml)
        for elem in root.iter("text"):
            text = elem.text
            if text:
                transcript_text.append(html.unescape(text).strip())
    except Exception as e:
        print("XML parse error:", e)

full_transcript = " ".join(transcript_text)
print("Transcript length:", len(full_transcript))
with open("scratch/full_transcript.txt", "w", encoding="utf-8") as f:
    f.write(full_transcript)
