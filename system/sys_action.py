import psutil
import win32gui
import win32process
import win32con
import win32com
import ctypes
import os
import win32api
import subprocess
from datetime import datetime
from colorama import Fore, Style,Back
from time import sleep

def open_Linken():
    try:
        exe_path = r"C:\Program Files (x86)\Linken Sphere 2\Linken Sphere 2.exe"
        working_dir = r"C:\Program Files (x86)\Linken Sphere 2"
        subprocess.Popen([exe_path], cwd=working_dir)
        return True
    except:
        return False
    
def is_app_running(process_name: str) -> bool:
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def resize_console(width=200, height=200):
    # Đặt lại kích thước CMD
    os.system(f'mode con: cols={width} lines={height}')

def move_and_pin_console_bottom_right(width_frac=3/7, height_frac=1/4):
    while True:
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()

            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)

            # Tính toán kích thước cửa sổ theo phần trăm màn hình
            window_width = int(screen_width * width_frac)
            window_height = int(screen_height * height_frac)

            # Tính vị trí ở góc dưới bên phải
            x = screen_width - window_width
            y = screen_height - window_height

            # Di chuyển cửa sổ tới vị trí
            win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)

            # Đặt cửa sổ luôn nằm trên cùng
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, window_width, window_height, win32con.SWP_SHOWWINDOW)

            # Thành công thì thoát
            break
        except:
            continue

def find_pid_by_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.pid:
            return conn.pid
    return None


def find_hwnd_by_pid(pid):
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def find_main_hwnd_by_pid(pid):
    def callback(hwnd, hwnds):
        try:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    hwnds.append(hwnd)
        except Exception:
            pass
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def find_main2_hwnd_by_pid(pid):
    def callback(hwnd, hwnds):
        try:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                title = win32gui.GetWindowText(hwnd)
                if win32gui.IsWindowVisible(hwnd) and title and "Restore" not in title:
                    hwnds.append(hwnd)
        except Exception:
            pass
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None


def get_window_position(i, col_limit=5, max_cols=4, offset_x=150, offset_y=30):
    col = (i // col_limit) % max_cols   # quay lại cột đầu khi quá max_cols
    row = i % col_limit
    x = col * offset_x
    y = row * offset_y
    return x, y

def bring_to_front_by_pid(pid):
    def enum_window_callback(hwnd, _):
        try:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid and win32gui.IsWindowVisible(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
        except:
            pass

    win32gui.EnumWindows(enum_window_callback, None)


def minimize_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def maximize_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(hwnd)

def maximize_window_not_foreground(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def foreground_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)


def restore_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
RESET = Style.RESET_ALL
def log(text, k):
    try:
        now = datetime.now().strftime("%H:%M:%S")
        color = COLORS[k % len(COLORS)]

        # Cố định độ rộng 12 ký tự cho "Thread k"
        thread_label = f"Thread {k}"
        thread_fixed = f"{thread_label:<10}"  # căn trái, 12 ký tự

        # Các phần hiển thị
        part_time = f"{Back.WHITE}{Fore.BLACK}[{now}] {RESET}"
        part_thread = f"{Back.GREEN}{Fore.WHITE} {thread_fixed} {RESET}"
        part_text = f" {Fore.WHITE}{text}{RESET}"

        print(f"{part_time}{part_thread}{part_text}")

    except Exception as e:
        print(f"{Back.RED}{Fore.WHITE}ERROR: log - {e}{RESET}")
