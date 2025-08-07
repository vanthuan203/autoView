from db.sqlite_utils import *
from api.api_utils import *
from api.api_section import *
from auto.auto import *
from system.sys_action import *
import pyautogui
import psutil
from time import sleep
import time
import threading
import random
import win32gui
import sys
import ctypes
from selenium import webdriver
from undetected_chromedriver import ChromeOptions


__version__ = "1.0.0"

ctypes.windll.kernel32.SetConsoleTitleW("AUTO")
init(autoreset=True)

queue = []
queue_open = []
queue_task = []
view_count = 0
false_count = 0
gui_count = 0
check_running = False

with open("NameVps.txt", "r", encoding="utf-8") as f:
    vps_name = f.readline().strip()


def update_console():
    try:
        try:
            global view_count, false_count, check_running, gui_count,__version__
            resize_console()
            move_and_pin_console_bottom_right()
        except:
            pass
        now = datetime.now().strftime("%H:%M:%S")
        while True:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                ram_percent = psutil.virtual_memory().percent
                title = (
                    f"{__version__} ⏰ TIME: {now} 🧠 CPU: {cpu_percent:.1f}% 💾 RAM: {ram_percent:.1f}% "
                    f"👁 VIEW: {view_count} ❌ FALSE: {false_count} 🖱 GUI: {gui_count}"
                )
                ctypes.windll.kernel32.SetConsoleTitleW(title)

                # Mỗi 60 giây cập nhật lại vị trí và kích thước cửa sổ
                if int(time.time()) % 60 == 0:
                    move_and_pin_console_bottom_right()
                    while True:
                        if active_preset("40f21312-257f-4885-ab31-141765220dc2"):
                            check_running = True
                            break
                        else:
                            if is_app_running("Linken Sphere"):
                                log("Linken Sphere hoạt động nhưng lỗi API đợi 30s...", -1)
                                sleep(30)
                                continue
                            else:
                                if open_Linken():
                                    log("Bật app Linken Sphere", -1)
                                    sleep(60)

                sleep(1)
            except:
                pass
    except:
        pass



def Thread_options(thread_id, accounts_chunk):
    for acc in accounts_chunk:
        login_account(acc, thread_id)


def chunk_accounts(accounts, num_chunks):
    # Chia đều và làm tròn lên
    chunk_size = (len(accounts) + num_chunks - 1) // num_chunks
    return [accounts[i:i + chunk_size] for i in range(0, len(accounts), chunk_size)]


def infinite_worker(thread_id):
    while True:
        try:
            queue_task.append(thread_id)
            sleep(random.uniform(3, 5))
            while queue_task[0] != thread_id:
                sleep(random.uniform(3, 5))
            task = get_task(vps_name)
            queue_task.remove(thread_id)
            if task == NULL:
                log("API Error...",-1)
                sleep(5)
                continue
            if (task["status"] == "true"):
                account = select_account(
                    f"email='{task['username']}' and live=1")
                if len(account) > 0:
                    task_account(account, thread_id,
                                 task['geo'], task['proxy'], task["video_id"], task["video_duration"], task["source"], task["video_title"], task["suggest_type"])
                else:
                    update_account_task(
                        task['username'], task["video_id"], False)
                    pass
            else:
                log("Không còn account để view!", thread_id)
                continue
            sleep(random.uniform(5, 10))  # Giả lập task định kỳ
        except:
            log("Lỗi threads!", thread_id)


def login_account(account, i):
    global view_count, false_count, check_running
    try:
        queue_open.append(i)  # open
        log("List OPEN: " + str(queue_open), i)
        email = str(account[0])
        uuid = str(account[3])
        while True:
            if check_running:
                break
            else:
                log("Đợi hệ thống hoạt động", i)
                sleep(10)
        if len(uuid) == 0:
            uuid = create_profile()
            if uuid != NULL:
                update_uuid_account(email, uuid)
                name_profile(uuid, email)
            else:
                false_count += 1
                log("Lỗi tạo profile", i)
                safe_remove(queue_open, i)
                return 0
        proxy_Check = False
        for _ in range(3):
            proxy_ran = get_proxy("vn")
            if proxy_ran != NULL:
                proxy = proxy_ran["proxy"].split(":")
                log("Add Proxy: "+proxy[0]+":"+proxy[1], i)
                if set_proxy(uuid, proxy):
                    if check_proxy(uuid):
                        proxy_Check = True
                        break

        if proxy_Check:
            pass
        else:
            false_count += 1
            safe_remove(queue_open, i)
            log("Lỗi add proxy", i)
            return 0

        # warmup_profile(uuid)
        port = start_profile(uuid)
        if port == NULL:
            sleep(10)
            port = start_profile(uuid)
            if port == NULL:
                false_count += 1
                safe_remove(queue_open, i)
                log("Lỗi start profile", i)
                return 0
        log("Start profile với port: "+str(port), i)
        try:
            # sleep(10)
            options = ChromeOptions()
            options.add_experimental_option(
                "debuggerAddress", f"127.0.0.1:{port}")
            # service = Service(executable_path=chromedriver_path)
            while queue_open[0] != i:
                sleep(random.uniform(2, 4))
            safe_remove(queue_open, i)
            driver = webdriver.Chrome(options=options)
            log("List OPEN: " + str(queue_open), i)
            for window in driver.window_handles:
                driver.switch_to.window(window)
                if driver.title != 'DevTools':
                    break
            # sleep(2)
            x, y = get_window_position(i)
            # i là chỉ số của trình duyệt
            driver.set_window_position(0, 0)
            # bạn có thể chỉnh kích thước theo nhu cầu
            driver.set_window_size(400, 800)
            driver.set_window_position(x, y)
            size = driver.get_window_size()

            pid = driver.service.process.pid  # đợi cửa sổ mở hoàn toàn
            bring_to_front_by_pid(pid)
            driver.set_window_position(x, y)
            sleep(2)
            driver.get('https://www.google.com/')
            sleep(random.uniform(3, 5))
            # original_hwnd = win32gui.GetForegroundWindow()
            # if original_hwnd:
            #    win32gui.SetForegroundWindow(original_hwnd)
            if driver is None:
                false_count += 1
                log("Không thể kết nối UC.", i)
                stop_profile(uuid, queue, queue_open, queue_task, email, i)
                log("Đã stop_profile.", i)
                return 0
            else:
                log("Kết nối UC thành công.", i)
                isLogin = login_gmail(account, driver, i)
                if isLogin != 1:
                    reset_account(email, 1)
                    delete_profile(uuid)
                    delete_account(email)
                driver.quit()
                stop_profile(uuid, queue, queue_open, queue_task, email, i)
                log("Đã stop_profile.", i)
                return 0
        except:
            false_count += 1
            log("Không thể mở trang.", i)
            sleep(5)
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
            return 0
    except Exception as e:
        false_count += 1
        log("Lỗi hệ thống!", i)
        try:
            driver.quit()
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
        except:
            try:
                driver.quit()
                stop_profile(uuid, queue, queue_open, queue_task, email, i)
                log("Đã stop_profile.", i)
            except:
                safe_remove(queue_open, i)
                pass


def task_account(account, i, geo, proxy_geo,video_id,video_duration,source,video_title,suggest_type):
    global view_count, false_count, check_running, gui_count
    try:
        index = 0
        email = str(account[0][0])
        uuid = str(account[0][3])
        queue_open.append(i)  # open
        log("List OPEN: " + str(queue_open), i)
        while True:
            if check_running:
                break
            else:
                log("Đợi hệ thống hoạt động", i)
                sleep(10)
        if len(uuid) == 0:
            uuid = create_profile()
            if uuid != NULL:
                update_uuid_account(email, uuid)
                name_profile(uuid, email)
            else:
                false_count += 1
                log("Lỗi tạo profile", i)
                safe_remove(queue_open, i)
                return 0
        # proxy
        proxy_Check = False
        proxy = proxy_geo.split(":")
        if set_proxy(uuid, proxy):
            if check_proxy(uuid):
                proxy_Check = True
        if not proxy_Check:
            for _ in range(3):
                proxy_ran = get_proxy(geo)
                if proxy_ran != NULL:
                    proxy = proxy_ran["proxy"].split(":")
                    if set_proxy(uuid, proxy):
                        if check_proxy(uuid):
                            proxy_Check = True
                            break
                sleep(5)

        if not proxy_Check:
            false_count += 1
            safe_remove(queue_open, i)
            log("Lỗi add proxy", i)
            return 0

        log("Add Proxy: "+proxy[0]+":"+proxy[1], i)

        # warmup_profile(uuid)
        port = start_profile(uuid)
        if port == NULL:
            sleep(10)
            port = start_profile(uuid)
            if port == NULL:
                false_count += 1
                safe_remove(queue_open, i)
                log("Lỗi start profile", i)
                return 0
        log("Start profile với port: "+str(port), i)
        try:
            # sleep(10)
            options = ChromeOptions()
            #options.add_argument("--start-maximized")
            # options.add_argument("--autoplay-policy=no-user-gesture-required")
            options.add_experimental_option(
                "debuggerAddress", f"127.0.0.1:{port}")
            while queue_open[0] != i:
                sleep(random.uniform(2, 4))
            safe_remove(queue_open, i)
            log("List OPEN: " + str(queue_open), i)
            driver = webdriver.Chrome(options=options)
            for window in driver.window_handles:
                driver.switch_to.window(window)
                if driver.title != 'DevTools':
                    break
            original_hwnd = win32gui.GetForegroundWindow()
            if original_hwnd:
                win32gui.SetForegroundWindow(original_hwnd)
            if driver is None:
                false_count += 1
                log("Không thể kết nối UC.", i)
                stop_profile(uuid, queue, queue_open, queue_task, email, i)
                log("Đã stop_profile.", i)
                return 0
            else:
                log("Kết nối UC thành công.", i)
                driver.minimize_window()
                driver.get("https://m.youtube.com")
                sleep(random.uniform(5, 7))
                log("Trang home thành công.", i)

                # video_id_ran = find_random_videoid(driver)
                # if video_id_ran:
                #     success = view(driver, email, port, uuid, i, video_id_ran, random.uniform(
                #         10, 15), "None", "", "fail")
                # else:
                #     success = pre_view(driver, email, port, uuid, i)
                success = view(driver, email, port, uuid, i, video_id, video_duration,source,video_title,suggest_type)
                while index < 4 and success:
                    task = get_task_by_account(vps_name, email)
                    if task == NULL:
                        log("API Error...",i)
                        sleep(15)
                        index += 1
                        continue
                    if (task["status"] == "true"):
                        account = select_account(
                            f"email='{task['username']}' and live=1")
                        if len(account) > 0:
                            success = view(
                                driver, email, port, uuid, i, task["video_id"], task["video_duration"], task["source"], task["video_title"], task["suggest_type"])
                            index += 1
                            continue
                        else:
                            update_account_task(
                                task['username'], task["video_id"], False)
                            break
                    else:
                        log("Không còn video để view lần "+str(index), i)
                        index += 1
                    sleep(random.uniform(5, 10))  # Giả lập task định kỳ
                try:
                    driver.quit()
                    stop_profile(uuid, queue, queue_open, queue_task, email, i)
                    log("Đã stop_profile.", i)
                except:
                    safe_remove(queue_open, i)
                    pass
                return 0
        except Exception as e:
            false_count += 1
            log("Lỗi hệ thống!", i)
            driver.quit()
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
            return 0
    except Exception as e:
        false_count += 1
        log("Lỗi hệ thống!", i)
        try:
            driver.quit()
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
        except:
            try:
                driver.quit()
                stop_profile(uuid, queue, queue_open, queue_task, email, i)
                log("Đã stop_profile.", i)
            except:
                safe_remove(queue_open, i)
                pass
    try:
        driver.quit()
        stop_profile(uuid, queue, queue_open, queue_task, email, i)
        log("Đã stop_profile.", i)
    except:
        safe_remove(queue_open, i)
        pass
    return 0


def view(driver, email, port, uuid, i, video_id, video_duration, source, keyword, suggest_type):
    try:
        try:
            log("Thực hiện view "+source, i)
            # source view
            if source == "suggest" and suggest_type == "fail" and 1==2:
                
                current_url = driver.current_url
                if "watch" in current_url:
                    pass
                else:
                    video_id_ran = find_random_videoid(driver)
                    if video_id_ran:
                        success = view(driver, email, port, uuid, i, video_id_ran, random.uniform(
                            10, 15), "None", keyword, suggest_type)
                        if not success:
                            stop_profile(uuid, queue, queue_open,
                                         queue_task, email, i)
                            log("Đã stop_profile.", i)
                            return False

                    else:
                        pass
            elif source == "suggest" and suggest_type == "true"  and 1==2:
                search_url = "https://m.youtube.com/results?search_query=" + \
                    "+".join(keyword.split())
                driver.get(search_url)
                log("Tìm kiếm video để đề xuất", i)
                sleep(random.uniform(5, 7))
                while True:
                    video_id_ran = find_random_videoid(driver)
                    if video_id_ran!=video_id:
                        break
                if video_id_ran:
                    success = view(driver, email, port, uuid, i, video_id_ran, random.uniform(
                        10, 25), "None", keyword, suggest_type)
                    if not success:
                        stop_profile(uuid, queue, queue_open,
                                     queue_task, email, i)
                        log("Đã stop_profile.", i)
                        return False
                else:
                    pass
            elif source == "dtn":
                current_url = driver.current_url
                if "watch" not in current_url:
                    pass
                else:
                    driver.get("https://m.youtube.com/")
                    log("Về trang home", i)
                    sleep(random.uniform(5, 7))
            elif source == "search":
                search_url = "https://m.youtube.com/results?search_query=" + \
                    "+".join(keyword.split())
                driver.get(search_url)
                log("Tìm kiếm video theo keyword", i)
                sleep(random.uniform(5, 7))

            global view_count, false_count, check_running, gui_count
            new_url = "https://m.youtube.com/watch?v="+video_id
            driver.execute_script(
                "window.location.href = arguments[0];", new_url)
            pid = find_pid_by_port(port)
            hwnd = find_main2_hwnd_by_pid(pid)
            if hwnd:
                try:
                    minimize_window(hwnd)
                    if win32gui.IsIconic(hwnd):
                        log("Đã minimize_window 0.", i)
                        queue.append(i)
                    else:
                        pid = find_pid_by_port(port)
                        hwnd = find_main2_hwnd_by_pid(pid)
                        minimize_window(hwnd)
                        if win32gui.IsIconic(hwnd):
                            log("Đã minimize_window 1.", i)
                            queue.append(i)
                        else:
                            false_count += 1
                            log("Không thể minimize_window.", i)
                            stop_profile(uuid, queue, queue_open,
                                         queue_task, email, i)
                            log("Đã stop_profile.", i)
                            return False
                except:
                    pid = find_pid_by_port(port)
                    hwnd = find_main2_hwnd_by_pid(pid)
                    minimize_window(hwnd)
                    if win32gui.IsIconic(hwnd):
                        log("Đã minimize_window 0.", i)
                        queue.append(i)
                    else:
                        pid = find_pid_by_port(port)
                        hwnd = find_main2_hwnd_by_pid(pid)
                        minimize_window(hwnd)
                        if win32gui.IsIconic(hwnd):
                            log("Đã minimize_window 1.", i)
                            queue.append(i)
                        else:
                            false_count += 1
                            log("Không thể minimize_window.", i)
                            stop_profile(uuid, queue, queue_open,
                                         queue_task, email, i)
                            log("Đã stop_profile.", i)
                            return False
        except:
            false_count += 1
            log("Không thể mở trang.", i)
            sleep(5)
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
            return False
        sleep(random.uniform(4, 6))
        while queue[0] != i:
            sleep(1)
        log("List GUI: " + str(queue), i)
        pid = find_pid_by_port(port)
        hwnd = find_main2_hwnd_by_pid(pid)
        if hwnd:
            try:
                maximize_window(hwnd)
                log("Đã maximize_window 0.", i)
            except:
                try:
                    pid = find_pid_by_port(port)
                    hwnd = find_main2_hwnd_by_pid(pid)
                    maximize_window(hwnd)
                    log("Đã maximize_window 1.", i)
                except:
                    false_count += 1
                    log("Không thể maximize_window.", i)
                    stop_profile(uuid, queue, queue_open, queue_task, email, i)
                    log("Đã stop_profile.", i)
                    return False
        sleep(random.uniform(2, 3))

        js = """
                const video = document.querySelector('video');
                if (video) {
                    return {
                        paused: video.paused,
                        muted: video.muted,
                        volume: video.volume,
                        currentTime: video.currentTime
                    };
                }
                return null;
                """
        result = driver.execute_script(js)
        if result:
            if (not result['muted']):
                log("Video không phát và có âm thanh.", i)
            else:
                log("Video có phát và không âm thanh. Run GUI 1", i)
                gui_count += 1
                width, height = pyautogui.size()
                original_hwnd = win32gui.GetForegroundWindow()
                pid = find_pid_by_port(port)
                hwnd = find_main2_hwnd_by_pid(pid)
                for _ in range(5):
                    if original_hwnd != hwnd:
                        win32gui.SetForegroundWindow(hwnd)
                        sleep(1)
                    else:
                        break
                pyautogui.moveTo(width/2+random.randint(1, 50), 250 +
                                 random.randint(1, 100), duration=random.uniform(0.2, 0.4))
                sleep(random.uniform(0.2, 0.4))
                pyautogui.leftClick()
                if bool(random.randint(0, 1)):
                    pyautogui.moveTo(width/2+random.randint(1, 300), 250 +
                                     random.randint(1, 300), duration=random.uniform(0.2, 0.4))
                else:
                    pyautogui.moveTo(width/2-random.randint(1, 300), 250 +
                                     random.randint(1, 300), duration=random.uniform(0.2, 0.4))
                sleep(random.uniform(2, 4))
                result = driver.execute_script(js)
                if result:
                    if (not result['paused']) and (not result['muted']):
                        log("Video không phát và có âm thanh.", i)
                    else:
                        log("Video có phát và không âm thanh. Run GUI 2", i)
                        original_hwnd = win32gui.GetForegroundWindow()
                        pid = find_pid_by_port(port)
                        hwnd = find_main2_hwnd_by_pid(pid)
                        for _ in range(5):
                            if original_hwnd != hwnd:
                                win32gui.SetForegroundWindow(hwnd)
                                sleep(1)
                            else:
                                break
                        pyautogui.moveTo(width/2+random.randint(1, 50), 250 +
                                         random.randint(1, 100), duration=random.uniform(0.2, 0.4))
                        sleep(random.uniform(0.3, 1))
                        pyautogui.leftClick()
                        if bool(random.randint(0, 1)):
                            pyautogui.moveTo(width/2+random.randint(1, 300), 250 +
                                             random.randint(1, 300), duration=random.uniform(0.2, 0.4))
                        else:
                            pyautogui.moveTo(width/2-random.randint(1, 300), 250 +
                                             random.randint(1, 300), duration=random.uniform(0.2, 0.4))
                        sleep(random.uniform(2, 4))
                        result = driver.execute_script(js)
                        if result:
                            if (not result['paused']) and (not result['muted']):
                                log("Video không phát và có âm thanh.", i)
                            else:
                                false_count += 1
                                log("Video có phát và không âm thanh. OFF", i)
                                stop_profile(uuid, queue, queue_open,
                                             queue_task, email, i)
                                log("Đã stop_profile.", i)
                                return False
        else:
            false_count += 1
            log("Không tìm thấy thẻ <video>.", i)
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
            return False
            # driver.get(new_url)
        safe_remove(queue, i)
        log("List GUI: " + str(queue), i)
        safe_remove(queue_open, i)
        log("List OPEN: " + str(queue_open), i)

        sleep(video_duration)
        if source != "None":
            view_count += 1
            log("Hoàn thành View!", i)
            if 1==1: #random.choice([True, False])
                driver.get("https://m.youtube.com")
                sleep(random.uniform(5, 7))
                log("Trang home thành công.", i)
            update_account_task(email, video_id, True)
        return True
    except:
        stop_profile(uuid, queue, queue_open, queue_task, email, i)
        log("Đã stop_profile.", i)
        return False


def pre_view(driver, email, port, uuid, i):
    try:
        try:
            global view_count, false_count, check_running, gui_count
            driver.get("https://m.youtube.com/shorts")
            pid = find_pid_by_port(port)
            hwnd = find_main2_hwnd_by_pid(pid)
            if hwnd:
                try:
                    minimize_window(hwnd)
                    if win32gui.IsIconic(hwnd):
                        log("Đã minimize_window 0.", i)
                        queue.append(i)
                    else:
                        pid = find_pid_by_port(port)
                        hwnd = find_main2_hwnd_by_pid(pid)
                        minimize_window(hwnd)
                        if win32gui.IsIconic(hwnd):
                            log("Đã minimize_window 1.", i)
                            queue.append(i)
                        else:
                            false_count += 1
                            log("Không thể minimize_window.", i)
                            stop_profile(uuid, queue, queue_open,
                                         queue_task, email, i)
                            log("Đã stop_profile.", i)
                            return False
                except:
                    pid = find_pid_by_port(port)
                    hwnd = find_main2_hwnd_by_pid(pid)
                    minimize_window(hwnd)
                    if win32gui.IsIconic(hwnd):
                        log("Đã minimize_window 0.", i)
                        queue.append(i)
                    else:
                        pid = find_pid_by_port(port)
                        hwnd = find_main2_hwnd_by_pid(pid)
                        minimize_window(hwnd)
                        if win32gui.IsIconic(hwnd):
                            log("Đã minimize_window 1.", i)
                            queue.append(i)
                        else:
                            false_count += 1
                            log("Không thể minimize_window.", i)
                            stop_profile(uuid, queue, queue_open,
                                         queue_task, email, i)
                            log("Đã stop_profile.", i)
                            return False
        except:
            false_count += 1
            log("Không thể mở trang.", i)
            sleep(5)
            stop_profile(uuid, queue, queue_open, queue_task, email, i)
            log("Đã stop_profile.", i)
            return False
        sleep(random.uniform(4, 6))
        while queue[0] != i:
            sleep(1)
        log("List PRE: " + str(queue), i)
        pid = find_pid_by_port(port)
        hwnd = find_main2_hwnd_by_pid(pid)
        if hwnd:
            try:
                maximize_window(hwnd)
                log("Đã maximize_window 0.", i)
            except:
                try:
                    pid = find_pid_by_port(port)
                    hwnd = find_main2_hwnd_by_pid(pid)
                    maximize_window_not_foreground(hwnd)
                    log("Đã maximize_window 1.", i)
                except:
                    false_count += 1
                    log("Không thể maximize_window.", i)
                    stop_profile(uuid, queue, queue_open, queue_task, email, i)
                    log("Đã stop_profile.", i)
                    return False
        safe_remove(queue, i)
        safe_remove(queue_open, i)
        sleep(random.uniform(5, 10))
        log("Hoàn thành Pre View", i)
        return True
    except:
        stop_profile(uuid, queue, queue_open, queue_task, email, i)
        log("Đã stop_profile.", i)
        return False


def main():
    global check_running
    while True:
        try:
            if getattr(sys, 'frozen', False):
                while True:
                    try:
                        threading.Thread(target=update_console,
                                         daemon=True).start()
                        break
                    except:
                        continue

            while True:
                if active_preset("40f21312-257f-4885-ab31-141765220dc2"):
                    check_running = True
                    log("Active Android Preset", -1)
                    break
                else:
                    if is_app_running("Linken Sphere"):
                        log("Linken Sphere hoạt động nhưng lỗi API đợi 30s...", -1)
                        sleep(30)
                        continue
                    else:
                        if open_Linken():
                            log("Bật app Linken Sphere", -1)
                            sleep(60)

            while True:
                try:
                    threads = 0
                    option = ""
                    mode = "auto"
                    delete_threads_vps(vps_name)
                    try:
                        while True:
                            try:
                                # check info VPS
                                data = check_vps(vps_name)
                                if data == NULL:
                                    log("API Error...", -1)
                                    sleep(5)
                                    continue
                                if (data["option"] == "Pending"):
                                    log("VPS Pending...", -1)
                                    sleep(5)
                                else:
                                    threads = data["threads"]
                                    option = data["option"]
                                    if data["vpsreset"] == 3:
                                        delete_account(None)
                                        log("Xóa all account...", -1)
                                    break
                            except:
                                sleep(5)
                                continue

                        while True:
                            account = get_account(vps_name, option)
                            if account == NULL:
                                log("API Error...", -1)
                                sleep(5)
                                continue
                            if (account["status"] == "true"):
                                insert_account(
                                    account["username"], account["password"], account["recover"])
                                log("Insert account: "+account["username"], -1)
                            else:
                                if "Đã đủ acc" in account["message"]:
                                    log("Đã đủ acount cho VPS!", -1)
                                    break
                            sleep(10)

                        accounts = select_account("live=0")
                        if len(accounts) > 0:
                            mode = "login"
                        if mode == "login":
                            chunks = chunk_accounts(accounts, 10)
                            thread_list = []
                            for i, acc_chunk in enumerate(chunks):
                                t = threading.Thread(
                                    target=Thread_options, args=(i, acc_chunk))
                                t.start()
                                sleep(random.uniform(30, 60))
                                thread_list.append(t)

                            for t in thread_list:
                                t.join()
                        loop_threads = []
                        for i in range(threads):
                            t = threading.Thread(target=infinite_worker,
                                                 args=(i,), daemon=True)
                            t.start()
                            sleep(random.uniform(30, 60))
                            loop_threads.append(t)

                        # Giữ main thread sống
                        try:
                            while True:
                                sleep(60)
                        except KeyboardInterrupt:
                            log("Dừng chương trình bởi người dùng.", -1)

                    except Exception as e:
                        log("Lỗi hàm main!", -1)
                except:
                    log("Lỗi hàm main!", -1)
        except:
            log("Lỗi hàm main!", -1)


if __name__ == "__main__":
    main()


# Threar
