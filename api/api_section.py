from api.api_utils import *
import requests
import json
from asyncio.windows_events import NULL
import os

def create_profile():
    try:
        x = {
            "count": 1
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/create_quick"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            data = json.loads(req.content)
            return data[0]["uuid"]
        else:
            return NULL
    except:
        return NULL


def name_profile(uuid, name):
    try:
        x = {
            "uuid": uuid,
            "name": name
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/set_name"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def set_proxy(uuid, proxy):
    try:
        x = {
            "uuid": uuid,
            "type": "http",
            "ip": proxy[0],
            "port": int(proxy[1]),
            "login": proxy[2],
            "password": proxy[3]
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/connection"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def start_profile(uuid):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ext_path = os.path.join(current_dir, 'ext')
        domain_google=r"*googlevideo.com*"
        domain_ip=r"*ipfighter.com*"
        #--proxy-bypass-list=*googlevideo.com*;*ipfighter.com*
        #--disable-extensions
        #f"--load-extension={ext_path} --proxy-bypass-list=*data.ssvd.online*"
        x = {
            "uuid": uuid,
            "chromium_args": f"--disable-extensions"
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/start"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            data = json.loads(req.content)
            return data.get("debug_port")
        else:
            return NULL
    except:
        return NULL


def stop_profile(uuid, queue, queue_open, queue_task, email, i):
    try:
        try:
            delete_threads_account(email)
        except:
            pass
        safe_remove(queue, i)
        safe_remove(queue_open, i)
        safe_remove(queue_task, i)
        x = {
            "uuid": uuid
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/stop"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def warmup_profile(uuid):
    try:
        x = {
            "uuid": uuid,
            "url_count": 7,
            "time_per_url": 3,
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/start_warmup"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def force_stop_profile(uuid):
    try:
        x = {
            "uuid": uuid,
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/force_stop"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def delete_profile(uuid):
    try:
        x = {
            "uuid": uuid,
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/delete"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def active_preset(uuid):
    try:
        x = {
            "uuid": uuid,
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/providers"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            return True
        else:
            return False
    except:
        False


def check_proxy(uuid):
    try:
        x = {
            "uuid": uuid,
        }
        header = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        url = "http://127.0.0.1:40080/sessions/check_proxy"
        req = requests.post(url, data=json.dumps(x), headers=header)
        if (req.status_code == 200):
            data = json.loads(req.content)
            if data.get("result") == "Success":
                return True
            else:
                return False
        else:
            return NULL
    except:
        return NULL


def safe_remove(queue, item):
    try:
        queue.remove(item)
    except ValueError:
        pass
