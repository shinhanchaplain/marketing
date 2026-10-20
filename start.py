import subprocess
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_dir)

print("=" * 60)
print("  AI 마케팅 자동화 스튜디오 대시보드를 실행합니다...")
print("=" * 60)

cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
subprocess.run(cmd)
