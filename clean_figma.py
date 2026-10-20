import os
import shutil
import subprocess
import time

def clean_reinstall_figma():
    print("=" * 60)
    print("  [피그마 완전 클린 재설치 마법사 - Python Core]")
    print("=" * 60)

    # 1. 프로세스 종료
    print("\n1. 실행 중인 피그마 프로세스를 종료합니다...")
    subprocess.run(["taskkill", "/F", "/IM", "Figma.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "Figma Agent.exe"], capture_output=True)
    time.sleep(1)

    # 2. 캐시 디렉터리 삭제
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    app_data = os.environ.get("APPDATA", "")

    figma_local = os.path.join(local_app_data, "Figma")
    figma_roaming = os.path.join(app_data, "Figma")

    print("\n2. 손상된 캐시 및 프로필 폴더를 완전히 삭제합니다...")
    if os.path.exists(figma_local):
        print(f"   - 삭제 중: {figma_local}")
        shutil.rmtree(figma_local, ignore_errors=True)
    else:
        print(f"   - 이미 정리됨: {figma_local}")

    if os.path.exists(figma_roaming):
        print(f"   - 삭제 중: {figma_roaming}")
        shutil.rmtree(figma_roaming, ignore_errors=True)
    else:
        print(f"   - 이미 정리됨: {figma_roaming}")

    # 3. 설치 프로그램 실행
    installer_path = r"d:\d드라이브\다운로드\FigmaSetup.exe"
    print("\n3. 최신 설치 프로그램(FigmaSetup.exe)을 실행합니다...")
    if os.path.exists(installer_path):
        print(f"   - 실행 경로: {installer_path}")
        subprocess.Popen([installer_path], shell=True)
        print("\n" + "=" * 60)
        print("  [성공] 클린 캐시 청소가 완료되었으며 피그마 설치가 시작되었습니다!")
        print("  잠시 후 피그마 로그인 창이 정상적으로 뜹니다.")
        print("=" * 60)
    else:
        print(f"\n[오류] 설치 파일을 찾을 수 없습니다: {installer_path}")

if __name__ == "__main__":
    clean_reinstall_figma()
