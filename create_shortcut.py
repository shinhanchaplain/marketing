import os
import win32com.client if False else None

# PowerShell 스크립트를 파일로 생성 후 실행
ps_code = """
$wsh = New-Object -ComObject WScript.Shell
$desktop1 = 'd:\\d드라이브\\바탕화면'
$shortcut1 = $wsh.CreateShortcut("$desktop1\\Figma.lnk")
$shortcut1.TargetPath = "$env:LOCALAPPDATA\\Figma\\Figma.exe"
$shortcut1.WorkingDirectory = "$env:LOCALAPPDATA\\Figma"
$shortcut1.Save()

# C드라이브 바탕화면에도 생성
$desktop2 = [Environment]::GetFolderPath('Desktop')
$shortcut2 = $wsh.CreateShortcut("$desktop2\\Figma.lnk")
$shortcut2.TargetPath = "$env:LOCALAPPDATA\\Figma\\Figma.exe"
$shortcut2.WorkingDirectory = "$env:LOCALAPPDATA\\Figma"
$shortcut2.Save()

Write-Host "Success"
"""

with open("create_shortcut.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)
print("Created script")
