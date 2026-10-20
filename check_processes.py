import subprocess

out = subprocess.check_output(['cmd', '/c', 'tasklist /v /fo csv | findstr /i figma'], text=True, errors='ignore')
for line in out.strip().splitlines():
    print(line)
