import subprocess
import time
import os

# 1. 크롬을 원격 디버깅 모드(포트 9222)로 실행하여 현재 피그마 세션을 제어할 수 있도록 설정
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# 현재 열려 있는 피그마 URL 대상
figma_url = "https://www.figma.com/files"

cmd = [
    chrome_path,
    "--remote-debugging-port=9222",
    "--user-data-dir=" + os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
    figma_url
]

print("Launching Chrome with remote debugging...")
subprocess.Popen(cmd)
time.sleep(3)
print("Chrome remote debugging ready.")
