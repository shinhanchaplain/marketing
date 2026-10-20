import ctypes
import ctypes.wintypes

user32 = ctypes.windll.user32

found_windows = []

def enum_windows_proc(hwnd, lParam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "figma" in title.lower():
                found_windows.append((hwnd, title))
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)

print(f"Total Figma Windows Found: {len(found_windows)}")
for hwnd, title in found_windows:
    print(f"HWND: {hwnd}, Title: '{title}'")
    # 창을 맨 앞으로 복원 및 최대화
    user32.ShowWindow(hwnd, 9) # 9 = SW_RESTORE
    user32.SetForegroundWindow(hwnd)
