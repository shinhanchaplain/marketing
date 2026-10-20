$wsh = New-Object -ComObject WScript.Shell

$dest1 = "d:\d드라이브\바탕화면\Figma.lnk"
$sc1 = $wsh.CreateShortcut($dest1)
$sc1.TargetPath = "$env:LOCALAPPDATA\Figma\Figma.exe"
$sc1.WorkingDirectory = "$env:LOCALAPPDATA\Figma"
$sc1.Save()

$dest2 = [Environment]::GetFolderPath('Desktop') + "\Figma.lnk"
$sc2 = $wsh.CreateShortcut($dest2)
$sc2.TargetPath = "$env:LOCALAPPDATA\Figma\Figma.exe"
$sc2.WorkingDirectory = "$env:LOCALAPPDATA\Figma"
$sc2.Save()

Write-Host "SHORTCUT_CREATED"
