import os
import requests
import sys

# API endpoint check update
API_URL = "http://your-server.com/check-update"  # đổi thành API của bạn

# Hàm lấy version từ file exe
def get_file_version(file_path):
    try:
        import win32api
        info = win32api.GetFileVersionInfo(file_path, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    except Exception as e:
        print(f"Lỗi lấy version: {e}")
        return None

# Hàm tìm file exe trong thư mục tool
def find_current_exe():
    for file in os.listdir(os.getcwd()):
        if file.lower().endswith(".exe"):
            return file
    return None

# Hàm check update và tải về
def check_and_update():
    exe_file = find_current_exe()
    if not exe_file:
        print("Không tìm thấy file exe trong thư mục hiện tại.")
        sys.exit(1)

    current_version = get_file_version(exe_file)
    if not current_version:
        print("Không lấy được version hiện tại.")
        sys.exit(1)

    print(f"Version hiện tại: {current_version}")

    try:
        # Gửi request kèm version hiện tại
        response = requests.get(API_URL, params={"version": current_version}, stream=True)

        if response.status_code == 200 and "application/octet-stream" in response.headers.get("Content-Type", ""):
            update_filename = exe_file  # ghi đè file cũ
            with open(update_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Đã tải và cập nhật file: {update_filename}")
        elif response.status_code == 204:
            print("Đang ở bản mới nhất. Không cần update.")
        else:
            print(f"Server trả về trạng thái {response.status_code}, không update.")
    except Exception as e:
        print(f"Lỗi khi check update: {e}")

if __name__ == "__main__":
    check_and_update()