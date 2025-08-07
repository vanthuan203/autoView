import requests
import json
from asyncio.windows_events import NULL
API_KEY="1"
API_URL="http://server1.idnetwork.com.vn/"
def check_vps(vps):
    params = {
        "vps": vps
    }

    req = requests.get(API_URL + "vps/checkvps", params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL
    
def get_account(vps,geo):
    params = {
        "vps": vps,
        "geo":geo
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "accview/get", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL
    

def get_proxy(geo):
    params = {
        "geo":geo
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "proxy/get_Rand_Proxy", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL    
    
def get_account_task(vps):
    params = {
        "vps": vps
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "historyview/getAccountTask", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL    
    
def get_task(vps):
    params = {
        "vps": vps
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "historyview/getview", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL    

def get_task_by_account(vps,username):
    params = {
        "vps": vps,
        "username":username
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "historyview/get", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL    

def update_account_task(username,videoid,success):
    params = {
        "username": username,
        "videoid":videoid,
        "success": success
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "historyview/update_Task28", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL   
    
def delete_threads_account(username):
    params = {
        "username": username
    }
    header = {
        "Authorization": API_KEY
    }
    req = requests.get(API_URL + "historyview/delthreadbyusername", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL   
    
def delete_threads_vps(vps):
    params = {
        "vps": vps
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "historyview/delnamebyvps", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL  

def reset_account(username,live):
    params = {
        "username": username,
        "live":live
    }
    header = {
        "Authorization": API_KEY,
    }
    req = requests.get(API_URL + "accview/resetaccountbyusername", headers=header, params=params)
    if (req.status_code == 200):
        data = json.loads(req.content)
        return data
    else:
        return NULL  