import ctypes
import ctypes.wintypes

user32 = ctypes.windll.user32

target_pids = {18980, 3784, 25548, 2528}

def enum_windows_proc(hwnd, lParam):
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in target_pids:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        
        # 창 표시 및 전면 배치
        user32.ShowWindow(hwnd, 5) # SW_SHOW
        user32.ShowWindow(hwnd, 9) # SW_RESTORE
        user32.SetWindowPos(hwnd, -1, 100, 100, 1200, 800, 0x0040) # HWND_TOPMOST
        user32.SetWindowPos(hwnd, -2, 100, 100, 1200, 800, 0x0040) # HWND_NOTOPMOST
        user32.SetForegroundWindow(hwnd)
        print(f"Brought window for PID {pid.value} to front! Title: '{buff.value}'")
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)
