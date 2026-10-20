import subprocess

svg_file = "figma_canvas_design.svg"
# SVG 파일로도 보관
with open(svg_file, "r", encoding="utf-8") as f:
    content = f.read()

# PowerShell로 완벽한 클립보드 주입
proc = subprocess.Popen(['powershell', '-Command', 'Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
proc.communicate(input=content)
print("CLIPBOARD_READY")
