from db.sqlite_utils import *
from system.sys_action import *
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from csv import reader
from datetime import datetime
# thêm:
from colorama import init, Fore, Style,Back
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def login_gmail(accounts,driver,k):

    email = accounts[0]
    log("Bắt đầu login "+email,k)
    password = accounts[1]
    recovery_mail = accounts[2]
    is_login = 0
    # try:
    driver.get('https://www.google.com/')
    sleep(random.uniform(3, 5))
    load_ggs = driver.find_elements(
        By.XPATH, '//input[contains(@class,"gLFyf gsfi")]')
    if (load_ggs):
        pass
    else:
        pass #WaitElement(driver, '//input[contains(@class,"gLFyf gsfi")]', 3)
    # đồng ý Cookike:
    sleep(3)
    checkcookie = driver.find_elements(
        By.XPATH, '//button[contains(@data-ved,"0ahUK") and contains(@id,"AGLb")]')
    if (checkcookie):
        el = driver.find_elements(By.XPATH, '//button[contains(@data-ved,"0ahUK") and contains(@id,"AGLb")]')[0]
        driver.execute_script("arguments[0].click();", el)
        sleep(3)
    # Login:
    checkLogin = driver.find_elements(
        By.XPATH, "//a[contains(@href,'ServiceLogin')]")

    if (checkLogin):
        try:
            ele = WebDriverWait(driver, 10).until(  # using explicit wait for 10 seconds
                EC.presence_of_element_located(
                    (By.XPATH,  "//a[contains(@href,'ServiceLogin')]"))  # finding the element
            )
            ele.click()
        except:
            try:
                ele = WebDriverWait(driver, 10).until(  # using explicit wait for 10 seconds
                    EC.presence_of_element_located(
                        (By.XPATH,  "//a[contains(@href,'ServiceLogin')]"))  # finding the element
                )
                ele.click()
            except:
                pass
        # tai khoan #
        check_capcha = 'True'
        check_type_email = driver.find_elements(
            By.XPATH, '//li//div[@jsname="rwl3qc"]')
        if (check_type_email):
            check_type_email[0].click()
        sleep(3)
        i = 0
        while (check_capcha == 'True' and i < 4):
            check_capcha = 'False'
            searchAnother = driver.find_elements(
                By.XPATH, '//li//div[@jsname="rwl3qc"]')
            if (searchAnother):
                searchAnother[0].click()
                sleep(3)
                WaitElement(driver, '//*[@id="identifierId"]', 3)

            # Nhập Email:
            seach_op = driver.find_element(
                By.XPATH, '//*[@id="identifierId"]')
            if (seach_op.is_displayed()):
                sleep(random.uniform(1, 3))
                typing(driver, email, seach_op)
                sleep(random.uniform(1, 3))
                seach_op.send_keys(Keys.ENTER)
                sleep(random.uniform(5, 10))
            # Check email không tồn tại:
            email_exit = driver.find_elements(
                By.XPATH, '//span[@class="jibhHc"]')
            if (email_exit):
                log("Email:("+email+") không tồn tại",k)
                update_live_account(email,3)
                return (is_login)
            # Xóa hoặc update lite = 4
            # Check Capcha:
            check_capcha = driver.find_element(
                By.XPATH, '//img[@id="captchaimg"]').is_displayed()
            if (check_capcha):
                i += 1
                check_capcha = 'True'
                driver.get('https://accounts.google.com/ServiceLogin/signinchooser?passive=1209600&continue=https%3A%2F%2Ftranslate.google.com%2F%3Fhl%3Dvi&followup=https%3A%2F%2Ftranslate.google.com%2F%3Fhl%3Dvi&hl=vi&ec=GAZAMw&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
                sleep(random.uniform(5, 7))
                continue
            seach_pass = driver.find_element(
                By.XPATH, '//input[@type="password"]')
            if (seach_pass.is_displayed()):
                # seach_pass.click()
                typing(driver, password, seach_pass)
                sleep(random.uniform(1, 2))
                seach_pass.send_keys(Keys.ENTER)
                sleep(random.uniform(3, 5))
                # check sai pass:
                wrong_pass = driver.find_elements(
                    By.XPATH, "//div[@jsname='B34EJ']//span")
                if (wrong_pass):
                    log("Email:("+email+") sai pass",k)
                    update_live_account(email,3)
                    return (is_login)
            # Check Capcha:
            check_capcha = driver.find_elements(
                By.XPATH, '//img[@id="captchaimg"]')
            if (check_capcha):
                check_capcha = driver.find_element(
                    By.XPATH, '//img[@id="captchaimg"]').is_displayed()
            check_toxic = driver.find_elements(
                By.XPATH, '//div[@class="CxRgyd"]//a[contains(@href,"support.google.com/accounts")]')
            if (check_toxic):
                check_toxic = driver.find_element(
                    By.XPATH, '//div[@class="CxRgyd"]//a[contains(@href,"support.google.com/accounts")]').is_displayed()
            check_xm = driver.find_elements(
                By.XPATH, '//div[@class="PrDSKc"]//a[contains(@href,"support.google.com/accounts/answer")]')
            if (check_xm):
                check_xm = driver.find_element(
                    By.XPATH, '//div[@class="PrDSKc"]//a[contains(@href,"support.google.com/accounts/answer")]').is_displayed()
            if (check_capcha or check_toxic or check_xm):
                i += 1
                check_capcha = 'True'
                driver.get('https://accounts.google.com/ServiceLogin/signinchooser?passive=1209600&continue=https%3A%2F%2Ftranslate.google.com%2F%3Fhl%3Dvi&followup=https%3A%2F%2Ftranslate.google.com%2F%3Fhl%3Dvi&hl=vi&ec=GAZAMw&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
                sleep(random.uniform(5, 7))
                continue
            # Check mail khôi phục
            seach_recovers = driver.find_elements(
                By.XPATH, "//form//li//div[@data-challengetype='12']")
            if (seach_recovers):
                seach_recover = driver.find_element(
                    By.XPATH, "//form//li//div[@data-challengetype='12']").is_displayed()
                if (seach_recover):
                    move_click(
                        driver, "//form//li//div[@data-challengetype='12']")
                    sleep(random.uniform(3, 5))
                    seach_op = driver.find_element(
                        By.XPATH, 'id("knowledge-preregistered-email-response")')
                    sleep(random.uniform(1, 2))
                    typing(driver, recovery_mail, seach_op)
                    driver.find_element(
                        By.XPATH, "//button[@type='button']").click()
                    sleep(random.uniform(3, 5))
            seach_fail_recover = driver.find_elements(
                By.XPATH, '//div[@class="LXRPh"]')
            if (seach_fail_recover):
                seach_fail_recovers = driver.find_element(
                    By.XPATH, '//div[@class="LXRPh"]').is_displayed()
                if (seach_fail_recovers):
                    update_live_account(email,6)
                    #  thoát và xóa profile
                    return (is_login)

        # Check không login dc do trình duyệt và mail khó:
        check_next = driver.find_elements(By.XPATH, 'id("next")')
        if (check_next):
            check_next = driver.find_element(
                By.XPATH, 'id("next")').is_displayed()
        check_reco = driver.find_elements(
            By.XPATH, 'id("accountRecoveryButton")')
        if (check_reco):
            check_reco = driver.find_element(
                By.XPATH, 'id("accountRecoveryButton")').is_displayed()
        if (check_next or check_reco):
            return (is_login)
            # thay profile hoặc finger.
        # Check đổi Pass:
        changer_pass = driver.find_elements(
            By.XPATH, '//input[@type="password"][@autocomplete="new-password"]')
        if (changer_pass):
            changer_pas = driver.find_element(
                By.XPATH, '//input[@type="password"][@autocomplete="new-password"]').is_displayed()
            if (changer_pas):
                new_pass = ("Chinh@("+password+")")
                move_click(driver, "(//input[@type='password'])[1]")
                typing(driver, new_pass, "(//input[@type='password'])[1]")
                sleep(random.uniform(1, 2))
                move_click(driver, "(//input[@type='password'])[2]")
                typing(driver, new_pass, "(//input[@type='password'])[2]")
                sleep(random.uniform(1, 2))
                doi_pass = driver.find_element(
                    By.XPATH, '//div[contains(@data-is-touch-wrapper,"true")]')
                if (doi_pass.is_displayed()):
                    doi_pass.click()
                else:
                    driver.find_element(
                        By.XPATH, '//div[(contains(@id,"passwordNext") or contains(@class,"N1UXxf"))]//button').click()
                sleep(random.uniform(3, 5))
                ok_pass = driver.find_element(
                    By.XPATH, '//button[@data-mdc-dialog-action="ok"]')
                if (ok_pass.is_displayed()):
                    ok_pass.click()
                    sleep(random.uniform(3, 5))
                nhap_pass = driver.find_element(
                    By.XPATH, '//input[@type="password"]').is_displayed()
                loi_pass = driver.find_element(
                    By.XPATH, '//div[@class="VfPpkd-fmcmS-yrriRe-W0vJo-RWgCYc"]/p[@id="i7"]').is_displayed()
                if (nhap_pass or loi_pass):
                    log(("Email:("+email+") lỗi Changer Pass"),k)
                    return (is_login)
                else:
                    pass
                    # update pass mới.
        # Check veryphone:
        veryphones = driver.find_elements(By.XPATH, 'id("deviceAddress")')
        if (veryphones):
            veryphone = driver.find_element(
                By.XPATH, 'id("deviceAddress")').is_displayed()
            if (veryphone):
                log(("Email:("+email+") Veryphone"),k)
                update_live_account(email,5)
                return (is_login)
        url = driver.execute_script('return document.URL;')

        # check bỏ qua địa chỉ và mail khôi phục
        if ("gds.google.com" in url):
            f_notnow = driver.find_elements(
                By.XPATH, '//div[@class="lq3Znf"]//button[contains(@class,"dgl2Hf ksBjEc")]')
            if (f_notnow):
                move_click(
                    driver, '//div[@class="lq3Znf"]//button[contains(@class,"dgl2Hf ksBjEc")]')
                sleep(random.uniform(3, 5))
            else:
                notnow = driver.find_elements(
                    By.XPATH, "(//div[@role='button' and @aria-disabled='false']//span)[1]")
                if (notnow):
                    move_click(
                        driver, "(//div[@role='button' and @aria-disabled='false']//span)[1]")
                    sleep(random.uniform(3, 5))

        # Check trang xác nhận/confirm:
        if ("myaccount.google.com/signinoptions/recovery-options-collection" in url):
            f_later = driver.find_elements(
                By.XPATH, '//div[@class="hgaXke VfPpkd-ksKsZd-XxIAqe"]')
            if (f_notnow):
                move_click(
                    driver, '//div[@class="hgaXke VfPpkd-ksKsZd-XxIAqe"]')
                sleep(random.uniform(5, 8))
            else:
                later = driver.find_elements(
                    By.XPATH, "((//div[@role='button'])[2]//span)[1]")
                if (later):
                    move_click(driver, "((//div[@role='button'])[2]//span)[1]")
                    sleep(random.uniform(5, 8))
        # Check bảng cuộn xong chọn Cookie:
        f_cookie = driver.find_elements(
            By.XPATH, '//img[contains(@src,"gstatic.com/ac/cb")]')
        if (f_cookie):
            driver.execute_script(
                'var scrollContainers = document.getElementsByClassName("J9h0d"); scrollContainers[0].scrollTop = 1000;')
            sleep(random.uniform(1, 2))
            driver.execute_script(
                'var scrollContainers = document.getElementsByClassName("J9h0d"); scrollContainers[0].scrollTop = 2000;')
            sleep(random.uniform(1, 2))
            driver.execute_script(
                'var scrollContainers = document.getElementsByClassName("J9h0d"); scrollContainers[0].scrollTop = 4000;')
            sleep(random.uniform(1, 2))
            driver.execute_script(
                'var scrollContainers = document.getElementsByClassName("J9h0d"); scrollContainers[0].scrollTop = 8000;')
            sleep(random.uniform(1, 2))
            driver.execute_script(
                'var scrollContainers = document.getElementsByClassName("J9h0d"); scrollContainers[0].scrollTop = 12000;')
            sleep(random.uniform(1, 2))
            driver.find_element(
                By.XPATH, '//span[@class="RveJvd snByac"]').click()
            sleep(random.uniform(5, 8))

# check domain
        try:
            ele = WebDriverWait(driver, 5).until(  # using explicit wait for 10 seconds
                EC.presence_of_element_located(
                    (By.XPATH, "//form[contains(@action,'gaplustos')]"))  # finding the element
            )
            try:
                ele = WebDriverWait(driver, 5).until(  # using explicit wait for 10 seconds
                    EC.presence_of_element_located(
                        (By.XPATH, "id('confirm')"))  # finding the element
                )
                sleep(random.uniform(1, 2))
                ele.click()
                sleep(random.uniform(5, 7))
            except:
                pass
        except:
            pass
        try:
            ele = WebDriverWait(driver, 5).until(  # using explicit wait for 10 seconds
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href,'enroll')]"))  # finding the element
            )
            try:
                ele = WebDriverWait(driver, 5).until(  # using explicit wait for 10 seconds
                    EC.presence_of_element_located(
                        (By.XPATH, "//a[contains(@href,'ServiceLogin')]"))  # finding the element
                )
                sleep(random.uniform(1, 2))
                driver.execute_script("arguments[0].click();", ele)
                sleep(random.uniform(5, 7))
            except:
                pass
        except:
            pass

        # check Birthday:
        url = driver.execute_script('return document.URL;')
        if ("birthday" in url):
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.randint(1880, 2004)
            c_day = driver.find_element(
                By.XPATH, '(//label//input[@type="text"])[1]').click()
            sleep(random.uniform(1, 2))
            day_nhap = driver.find_element(
                By.XPATH, '//label//input[@type="text"])[1]')
            typing(driver, str(day), day_nhap)
            sleep(random.uniform(1, 3))
            driver.find_element(
                By.XPATH, '//div[@aria-haspopup="listbox"]').click()
            sleep(random.uniform(1, 2))
            driver.find_element(
                By.XPATH, '//li[@data-value='+'\''+str(month)+'\''+']').click()
            sleep(random.uniform(1, 3))
            c_year = driver.find_element(
                By.XPATH, '(//label//input[@type="text"])[2]').click()
            year_nhap = driver.find_element(
                By.XPATH, '//label//input[@type="text"])[2]')
            typing(driver, str(year), year_nhap)
            f_birthday = driver.find_elements(
                By.XPATH, '//button[@type="submit" or @jsname="x8hlje"]')
            if (f_birthday):
                f_birthday[0].click()
                sleep(random.uniform(1, 2))
                driver.find_element(
                    By.XPATH, '//button[@data-mdc-dialog-action="ok"]//div').click()
                sleep(random.uniform(1, 2))
                driver.find_element(
                    By.XPATH, '//button[contains(@class,"k1rdg")]').click()
                f_bir = driver.find_elements(
                    By.XPATH, '//button[@jsname="AHldd"]')
                if (f_bir):
                    f_bir[0].click()
                else:
                    driver.find_element(
                        By.XPATH, '//button[contains(@class,"DuMIQc qfvgSe EzK3ye")]').click()
                    sleep(random.uniform(1, 2))
                    driver.find_element(
                        By.XPATH, '//button[contains(@class,"VfPpkd-ksKsZd-mWPk3d")]').click()
                    sleep(random.uniform(1, 2))
                    driver.find_element(
                        By.XPATH, '//button[contains(@class,"k1rdg")]').click()
                sleep(random.uniform(5, 10))

        # check bật nhật ký:
        diary = driver.find_elements(
            By.XPATH, '//img[contains(@src,"youtube.com/img/home/blank_homepage")]')
        if (diary):
            driver.find_element(
                By.XPATH, '//tp-yt-paper-button[@class="style-scope ytd-button-renderer style-primary size-default"]').click()
            sleep(random.uniform(5, 8))
        btsd = driver.find_elements(
            By.XPATH, '//yt-formatted-string[@class="style-scope yt-button-renderer style-blue-text size-default"]')
        if (btsd):
            btsd[0].click()

    load_url(driver, email, "https://www.google.com/",
             '//input[contains(@class,"gLFyf gsfi")]',)
    sleep(random.uniform(1, 3))
    checkLogins = driver.find_elements(
        By.XPATH, "//a[contains(@href,'SignOutOptions')]")
    if (checkLogins):
        log(email+" login Google OK!",k)
        #review(driver)
        # checklogin Youtube
        driver.get('https://www.youtube.com/')
        # check load YTB:
        sleep(random.uniform(3, 5))
        avar_button = driver.find_elements(
            By.XPATH, '//img[contains(@src,"yt3.ggpht.com")] | //yt-avatar-shape')
        if (avar_button):
            driver.execute_script("arguments[0].click();", avar_button[0])
            sleep(random.uniform(3, 5))
        else:
            WaitElement(
                driver, '//img[contains(@src,"yt3.ggpht.com")] | //yt-avatar-shape', 3)
            sleep(3)
        # check nhiều kênh:
        avar_button = driver.find_elements(
            By.XPATH, '//img[contains(@src,"yt3.ggpht.com")] | //yt-avatar-shape')
        if (avar_button):
            driver.execute_script("arguments[0].click();", avar_button[0])
            sleep(random.uniform(3, 5))
        else:
            WaitElement(
                driver, '//img[contains(@src,"yt3.ggpht.com")] | //yt-avatar-shape', 3)
            sleep(random.uniform(3, 5))
        switch_button = driver.find_elements(
            By.XPATH, '//button[contains(@class,"next--size-s")]')
        if (switch_button):
            driver.execute_script("arguments[0].click();", switch_button[0])
            sleep(random.uniform(3, 5))
        else:
            WaitElement(
                driver, '//button[contains(@class,"next--size-s")]', 3)
            sleep(3)
        kth_button = driver.find_elements(
            By.XPATH, '(//ytm-account-item-section-renderer//span[contains(text(),"@")])[last()]')
        if (kth_button):
            driver.execute_script("arguments[0].click();", kth_button[0])
            sleep(random.uniform(3, 5))
        else:
            WaitElement(
                driver, '(//ytm-account-item-section-renderer//span[contains(text(),"@")])[last()]', 3)
            sleep(3)
        url = driver.execute_script('return document.URL;')
        # Check mail vô hiệu hóa:
        if ("disabled" in url or "oops" in url or "support.google.com" in url):
            i = 0
            while (i < 3):
                i += 1
                load_url(driver, email, 'https://www.youtube.com',
                         '//a[contains(@href,"/watch?v")]')
                url = driver.execute_script('return document.URL;')
                if ("disabled" in url or "oops" in url or "support.google.com" in url):
                    log("Email:("+email+") vô hiệu hóa YTB",k)
                    update_live_account(email,4)
                    return (is_login)
        if ('https://www.youtube.com' in url):
            pass
        else:
            load_url(driver, email, 'https://www.youtube.com/',
                     '//a[contains(@href,"/watch?v")]')

        loginytb = driver.find_elements(
            By.XPATH, '//a[contains(@href,"https://accounts.google.com/ServiceLogin")]')
        if (loginytb):
            move_click(
                driver, '//a[contains(@href,"https://accounts.google.com/ServiceLogin")]')
            sleep(random.uniform(3, 6))
        loginytb = driver.find_elements(
            By.XPATH, '//a[contains(@href,"https://accounts.google.com/ServiceLogin")]')
        if (loginytb):
            update_live_account(email,0)
            sleep(random.uniform(3, 6))
            return (is_login)
        else:
            is_login = 1
            log("Email: "+email+" login Y OK!",k)
            update_live_account(email,1)
            return (is_login)
    else:
        log(email+" đăng nhập fail!",k)
        sleep(random.uniform(15, 20))
        # delete_profile(profile_id)
        update_live_account(email,0)
    # except:
        # sleep(random.uniform(1, 2))
        # return(is_login)


def load_url(driver, email, url, xpath,):
    driver.get(url)
    sleep(random.uniform(3, 5))
    load_urls = driver.find_elements(By.XPATH, xpath)
    if (load_urls):
        pass
    else:
        WaitElement(driver, xpath, 3)
        sleep(3)

def referrer_url(driver,video_id):
    try:
        target_video = "/watch?v="+video_id
        js = f"""
        const TARGET_VIDEO = "{target_video}";

        // 1. Chờ DOM sẵn sàng
        function waitForVideosAndClick() {{
        const links = Array.from(document.querySelectorAll('a[href*="/watch?v="]'));

        if (links.length === 0) {{
            // Nếu chưa có video, thử lại sau 300ms
            setTimeout(waitForVideosAndClick, 300);
            return false;
        }}

        // 2. Thay toàn bộ href thành video đích
        links.forEach(link => {{
            link.href = TARGET_VIDEO;
            link.setAttribute("href", TARGET_VIDEO);

            // Tạo clone để xóa event listener của YouTube
            const cleanLink = link.cloneNode(true);
            link.replaceWith(cleanLink);
        }});

        // 3. Click vào video đầu tiên (sau khi đã thay href)
        const first = document.querySelector('a[href*="/watch?v="]');
        if (first) {{
            first.click();
            return true;
        }} else {{
            return false;
        }}
        }}

        // Bắt đầu chạy
        return waitForVideosAndClick();
        """
        result = driver.execute_script(js)
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
def WaitElement(driver, ele, i):
    j = 0
    while (True):
        j = j+1
        checkEle = driver.find_elements(By.XPATH, ele)
        if (checkEle):
            break
        else:
            sleep(3)
            if (j <= i):
                continue
            else:
                break

def typing(driver, text, xpath):
    texts = list(text)
    for j in range(len(texts)):
        xpath.send_keys(texts[j])
        sleep(random.uniform(0.1, 0.3))

def move_click(driver, element):
    elements = driver.find_element(By.XPATH, element)
    driver.execute_script("arguments[0].scrollIntoView(true);", elements)
    sleep(random.uniform(1, 3))
    driver.execute_script("arguments[0].click();", elements)
    sleep(random.uniform(2, 4))

def find_random_videoid(driver):
    try:
        # Đợi cho tới khi có ít nhất 1 thumbnail xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a#thumbnail[href*='watch?v=']"))
        )

        js_script = r"""
            let anchors = Array.from(document.querySelectorAll('a#thumbnail[href*="watch?v="]'));
            let videoIds = anchors
                .map(a => {
                    let href = a.getAttribute('href');
                    let match = href ? href.match(/v=([\w-]{11})/) : null;
                    return match ? match[1] : null;
                })
                .filter(id => id);

            return [...new Set(videoIds)];
        """
        video_ids = driver.execute_script(js_script)
        return random.choice(video_ids) if video_ids else None

    except:
        return None



def build_js_script(video_id: str, title: str) -> str:
    return f"""(() => {{
  // ===== CẤU HÌNH =====
  const TO_VIDEO_ID = "{video_id}"; // ID muốn thay (11 ký tự)
  const NEW_TITLE   = "{title}";    // để '' nếu không muốn ép tiêu đề

  // ===== UTILS =====
  const ID_RE = /^[A-Za-z0-9_-]{{11}}$/;
  const isId = s => typeof s === 'string' && ID_RE.test((s || '').trim());
  const toStr = v => String(v ?? '');

  const isBrowse = u => typeof u === 'string' && u.includes('/youtubei/v1/browse');
  const isSearch = u => typeof u === 'string' && u.includes('/youtubei/v1/search');
  const isNext   = u => typeof u === 'string' && u.includes('/youtubei/v1/next');

  const moveItemToFront = (arr, idx) => {{
    if (!Array.isArray(arr) || idx <= 0 || idx >= arr.length) return 0;
    arr.unshift(arr.splice(idx, 1)[0]);
    return 1;
  }};

  // Chuẩn hoá /watch?…v=<fromId>… -> /watch?v=<toId> (giữ domain nếu có, cắt sạch query sau)
  function canonicalWatch(u, fromId, toId) {{
    return toStr(u)
      .replace(
        new RegExp(`((?:https?:\\/\\/[^\\s"'<>]+)?)\\/watch\\?[^\\s"'<>]*\\bv=${{fromId}}[^\\s"'<>]*`, 'g'),
        (_, pre) => `${{pre}}/watch?v=${{toId}}`
      )
      .replace(new RegExp(`(\\/watch\\?v=${{toId}})[^\\s"'<>)]*`, 'g'), '$1');
  }}

  function rewriteUrls(s, fromId, toId) {{
    let out = String(s);
    out = out.replace(new RegExp(`(/watch\\?v=)${{fromId}}(?:[&?#][^"'\\s]*)?`, 'g'), `$1${{toId}}`);
    out = out.replace(new RegExp(`(/shorts/)${{fromId}}(?:[?&#][^"'\\s]*)?`, 'g'), `/watch?v=${{toId}}`);
    out = out.replace(new RegExp(`(i\\.ytimg\\.com/vi/)${{fromId}}(?=/)`, 'g'), `$1${{toId}}`);
    out = out.replace(new RegExp(`(i\\.ytimg\\.com/vi_webp/)${{fromId}}(?=/)`, 'g'), `$1${{toId}}`);
    return out;
  }}

  function isShortsNode(node) {{
    const re = /\/shorts\//;
    const st = [node];
    while (st.length) {{
      const cur = st.pop();
      if (!cur) continue;
      if (typeof cur === 'string') {{ if (re.test(cur)) return true; }}
      else if (Array.isArray(cur)) {{ for (const v of cur) st.push(v); }}
      else if (typeof cur === 'object') {{ for (const v of Object.values(cur)) st.push(v); }}
    }}
    return false;
  }}

  function textHas(obj, needle) {{
    const s = toStr(needle);
    if (!obj) return false;
    if (typeof obj === 'string') return obj.includes(s);
    if (typeof obj.content === 'string') return obj.content.includes(s);
    if (typeof obj.text === 'string') return obj.text.includes(s);
    if (Array.isArray(obj.runs)) return obj.runs.some(r => toStr(r?.text).includes(s));
    if (typeof obj.simpleText === 'string') return obj.simpleText.includes(s);
    return false;
  }}

  function findFirstVideoId(root) {{
    const st = [root];
    while (st.length) {{
      const cur = st.pop();
      if (!cur) continue;
      if (Array.isArray(cur)) {{
        for (const v of cur) if (v && (typeof v === 'object' || Array.isArray(v))) st.push(v);
      }} else if (typeof cur === 'object') {{
        const we = cur?.watchEndpoint;
        if (we?.videoId && isId(we.videoId)) return we.videoId;
        if (cur?.videoId && isId(cur.videoId)) return cur.videoId;
        if (cur?.contentId && isId(cur.contentId)) return cur.contentId;
        for (const v of Object.values(cur)) if (v && (typeof v === 'object' || Array.isArray(v))) st.push(v);
      }}
    }}
    return null;
  }}

  function walk(node, cb) {{
    const st = [node];
    while (st.length) {{
      const cur = st.pop();
      if (!cur) continue;
      if (Array.isArray(cur)) {{
        for (let i = 0; i < cur.length; i++) {{
          cb(cur, i, cur[i]);
          if (cur[i] && typeof cur[i] === 'object') st.push(cur[i]);
        }}
      }} else if (typeof cur === 'object') {{
        for (const [k, v] of Object.entries(cur)) {{
          cb(cur, k, v);
          if (v && typeof v === 'object') st.push(v);
        }}
      }}
    }}
  }}

  function setText(obj, txt) {{
    if (!obj || typeof obj !== 'object') return 0;
    let c = 0;
    if (typeof obj.content === 'string') {{ obj.content = txt; c++; }}
    if ('simpleText' in obj)            {{ obj.simpleText = txt; c++; }}
    if (Array.isArray(obj.runs))        {{ obj.runs = [{{ text: txt }}]; c++; }}
    if (typeof obj.text === 'string')   {{ obj.text = txt; c++; }}
    return c;
  }}

  function forceSetAllTitles(root, newTitle) {{
    let count = 0;
    walk(root, (obj, key, val) => {{
      if (!val || typeof val !== 'object') return;
      if (['title','headline','contentTitle','formattedTitle','titleText','videoTitle'].includes(key)) {{
        count += setText(val, newTitle);
      }}
      if (key === 'metadata') {{
        if (Array.isArray(val)) {{
          for (const m of val) {{
            count += setText(m?.title, newTitle);
            count += setText(m?.primaryText, newTitle);
            count += setText(m?.lockupMetadataViewModel?.title, newTitle);
          }}
        }} else if (val && typeof val === 'object') {{
          count += setText(val?.title, newTitle);
          count += setText(val?.primaryText, newTitle);
          count += setText(val?.lockupMetadataViewModel?.title, newTitle);
        }}
      }}
    }});
    return count;
  }}

  // ====== FINDERS: trả về cả parent array + index để có thể move-to-front ======
  function getFirstHomeVideoNode(root) {{
    // Desktop: twoColumn → richGridRenderer
    try {{
      const tabs = root?.contents?.twoColumnBrowseResultsRenderer?.tabs;
      const contents = tabs?.find(t => t?.tabRenderer?.selected)
                           ?.tabRenderer?.content?.richGridRenderer?.contents;
      if (Array.isArray(contents) && contents.length) {{
        const firstItem = contents[0];
        const lv0 = firstItem?.richItemRenderer?.content?.lockupViewModel;
        if (lv0?.contentType === 'LOCKUP_CONTENT_TYPE_VIDEO' && isId(lv0?.contentId) && !isShortsNode(firstItem)) {{
          return {{ node: firstItem, videoId: lv0.contentId, parent: contents, index: 0 }};
        }}
        for (let i = 0; i < contents.length; i++) {{
          const item = contents[i];
          const lv = item?.richItemRenderer?.content?.lockupViewModel;
          if (lv?.contentType === 'LOCKUP_CONTENT_TYPE_VIDEO' && isId(lv?.contentId) && !isShortsNode(item)) {{
            return {{ node: item, videoId: lv.contentId, parent: contents, index: i }};
          }}
          const vr = item?.richItemRenderer?.content?.videoRenderer;
          if (vr?.videoId && isId(vr.videoId) && !isShortsNode(item)) {{
            return {{ node: item, videoId: vr.videoId, parent: contents, index: i }};
          }}
          const vwc = item?.richItemRenderer?.content?.videoWithContextRenderer;
          if (vwc) {{
            const id = vwc?.navigationEndpoint?.watchEndpoint?.videoId
                    || vwc?.videoId
                    || vwc?.inlinePlaybackEndpoint?.watchEndpoint?.videoId
                    || findFirstVideoId(vwc);
            if (isId(id) && !isShortsNode(item)) return {{ node: item, videoId: id, parent: contents, index: i }};
          }}
        }}
      }}
    }} catch {{}}

    // Mobile: singleColumn → richGridRenderer
    try {{
      const scTabs = root?.contents?.singleColumnBrowseResultsRenderer?.tabs;
      if (Array.isArray(scTabs)) {{
        for (const t of scTabs) {{
          const tab = t?.tabRenderer;
          if (!tab?.selected) continue;
          const contents = tab?.content?.richGridRenderer?.contents;
          if (!Array.isArray(contents)) continue;
          for (let i = 0; i < contents.length; i++) {{
            const item = contents[i];
            const v = item?.richItemRenderer?.content?.videoWithContextRenderer;
            if (v) {{
              const id = v?.navigationEndpoint?.watchEndpoint?.videoId
                      || v?.videoId
                      || v?.inlinePlaybackEndpoint?.watchEndpoint?.videoId
                      || findFirstVideoId(v);
              if (isId(id) && !isShortsNode(item)) return {{ node: item, videoId: id, parent: contents, index: i }};
            }}
          }}
        }}
      }}
    }} catch {{}}
    return null;
  }}

  function getFirstSearchVideoNode(root) {{
    // Desktop
    try {{
      const sections = root?.contents?.twoColumnSearchResultsRenderer
        ?.primaryContents?.sectionListRenderer?.contents;
      if (Array.isArray(sections)) {{
        for (const sec of sections) {{
          const items = sec?.itemSectionRenderer?.contents;
          if (!Array.isArray(items)) continue;
          for (let i = 0; i < items.length; i++) {{
            const it = items[i];
            const vr = it?.videoRenderer;
            if (vr?.videoId && isId(vr.videoId) && !isShortsNode(it)) {{
              return {{ node: it, videoId: vr.videoId, parent: items, index: i }};
            }}
            const vwc = it?.videoWithContextRenderer;
            if (vwc) {{
              const id = vwc?.navigationEndpoint?.watchEndpoint?.videoId
                      || vwc?.videoId
                      || vwc?.inlinePlaybackEndpoint?.watchEndpoint?.videoId
                      || findFirstVideoId(vwc);
              if (isId(id) && !isShortsNode(it)) return {{ node: it, videoId: id, parent: items, index: i }};
            }}
          }}
        }}
      }}
    }} catch {{}}

    // Mobile
    try {{
      const sections = root?.contents?.sectionListRenderer?.contents;
      if (Array.isArray(sections)) {{
        for (const sec of sections) {{
          const items = sec?.itemSectionRenderer?.contents;
          if (!Array.isArray(items)) continue;
          for (let i = 0; i < items.length; i++) {{
            const it = items[i];
            const vwc = it?.videoWithContextRenderer;
            if (vwc) {{
              const id = vwc?.navigationEndpoint?.watchEndpoint?.videoId || vwc?.videoId;
              if (isId(id) && !isShortsNode(it)) return {{ node: it, videoId: id, parent: items, index: i }};
            }}
            const vr = it?.videoRenderer;
            if (vr?.videoId && isId(vr.videoId) && !isShortsNode(it)) {{
              return {{ node: it, videoId: vr.videoId, parent: items, index: i }};
            }}
          }}
        }}
      }}
    }} catch {{}}
    return null;
  }}

  function findNodeByTitle(root, title) {{
    const t = toStr(title).trim();
    if (!t) return null;

    // browse desktop/mobile
    try {{
      const grids = [
        root?.contents?.twoColumnBrowseResultsRenderer?.tabs?.find(x => x?.tabRenderer?.selected)?.tabRenderer?.content?.richGridRenderer?.contents,
        root?.contents?.singleColumnBrowseResultsRenderer?.tabs?.find(x => x?.tabRenderer?.selected)?.tabRenderer?.content?.richGridRenderer?.contents,
      ].filter(Boolean);

      for (const contents of grids) {{
        for (let i = 0; i < contents.length; i++) {{
          const item = contents[i];
          if (isShortsNode(item)) continue;
          const lv = item?.richItemRenderer?.content?.lockupViewModel;
          if (lv?.contentType === 'LOCKUP_CONTENT_TYPE_VIDEO') {{
            if (textHas(lv?.title, t) || textHas(lv?.metadata?.title, t)) {{
              const vid = lv?.contentId || findFirstVideoId(item);
              if (isId(vid)) return {{ node: item, videoId: vid, parent: contents, index: i }};
            }}
          }}
          const v = item?.richItemRenderer?.content?.videoWithContextRenderer;
          if (v && (textHas(v?.headline, t) || textHas(v?.title, t))) {{
            const vid = v?.navigationEndpoint?.watchEndpoint?.videoId
                     || v?.videoId
                     || v?.inlinePlaybackEndpoint?.watchEndpoint?.videoId
                     || findFirstVideoId(v);
            if (isId(vid)) return {{ node: item, videoId: vid, parent: contents, index: i }};
          }}
          const vr = item?.richItemRenderer?.content?.videoRenderer;
          if (vr && textHas(vr?.title, t) && isId(vr?.videoId)) {{
            return {{ node: item, videoId: vr.videoId, parent: contents, index: i }};
          }}
        }}
      }}
    }} catch {{}}

    // search desktop
    try {{
      const sections = root?.contents?.twoColumnSearchResultsRenderer
        ?.primaryContents?.sectionListRenderer?.contents;
      if (Array.isArray(sections)) {{
        for (const sec of sections) {{
          const items = sec?.itemSectionRenderer?.contents;
          if (!Array.isArray(items)) continue;
          for (let i = 0; i < items.length; i++) {{
            const it = items[i];
            if (isShortsNode(it)) continue;
            const vr = it?.videoRenderer;
            if (vr && textHas(vr?.title, t) && isId(vr?.videoId)) {{
              return {{ node: it, videoId: vr.videoId, parent: items, index: i }};
            }}
            const v = it?.videoWithContextRenderer;
            if (v && (textHas(v?.headline, t) || textHas(v?.title, t))) {{
              const vid = v?.navigationEndpoint?.watchEndpoint?.videoId
                       || v?.videoId
                       || v?.inlinePlaybackEndpoint?.watchEndpoint?.videoId
                       || findFirstVideoId(v);
              if (isId(vid)) return {{ node: it, videoId: vid, parent: items, index: i }};
            }}
          }}
        }}
      }}
    }} catch {{}}

    // search mobile
    try {{
      const sections = root?.contents?.sectionListRenderer?.contents;
      if (Array.isArray(sections)) {{
        for (const sec of sections) {{
          const items = sec?.itemSectionRenderer?.contents;
          if (!Array.isArray(items)) continue;
          for (let i = 0; i < items.length; i++) {{
            const it = items[i];
            if (isShortsNode(it)) continue;
            const v = it?.videoWithContextRenderer;
            if (v && textHas(v?.headline, t)) {{
              const vid = v?.navigationEndpoint?.watchEndpoint?.videoId || v?.videoId || findFirstVideoId(v);
              if (isId(vid)) return {{ node: it, videoId: vid, parent: items, index: i }};
            }}
            const vr = it?.videoRenderer;
            if (vr && textHas(vr?.title, t) && isId(vr?.videoId)) {{
              return {{ node: it, videoId: vr.videoId, parent: items, index: i }};
            }}
          }}
        }}
      }}
    }} catch {{}}
    return null;
  }}

  // /next (đề xuất)
  function getFirstMobileRecItem(root) {{
    try {{
      const results = root?.contents?.singleColumnWatchNextResults?.results?.results?.contents;
      if (!Array.isArray(results)) return null;
      for (const block of results) {{
        const items = block?.itemSectionRenderer?.contents;
        if (!Array.isArray(items)) continue;
        for (let i = 0; i < items.length; i++) {{
          const it = items[i];
          const v = it?.videoWithContextRenderer;
          const vid = v?.videoId || v?.navigationEndpoint?.watchEndpoint?.videoId;
          if (v && isId(vid)) return {{ node: v, videoId: vid, parent: items, index: i }};
        }}
      }}
    }} catch {{}}
    return null;
  }}

  function getFirstDesktopRecItem(root) {{
    try {{
      const sec = root?.contents?.twoColumnWatchNextResults?.secondaryResults?.secondaryResults?.results;
      if (Array.isArray(sec)) {{
        const t = scanItemSectionArray(sec);
        if (t) return t;
      }}
      const eps = root?.onResponseReceivedEndpoints;
      if (Array.isArray(eps)) {{
        for (const ep of eps) {{
          const cont = ep?.appendContinuationItemsAction?.continuationItems
                    || ep?.reloadContinuationItemsCommand?.continuationItems;
          if (!Array.isArray(cont)) continue;
          const t = scanItemSectionArray(cont);
          if (t) return t;
        }}
      }}
    }} catch {{}}
    return null;
  }}

  function scanItemSectionArray(arr) {{
    for (const r of arr) {{
      const items = r?.itemSectionRenderer?.contents;
      if (!Array.isArray(items)) continue;
      for (let i = 0; i < items.length; i++) {{
        const it = items[i];
        const cv = it?.compactVideoRenderer;
        if (cv?.videoId && isId(cv.videoId)) return {{ node: cv, videoId: cv.videoId, parent: items, index: i }};
        const lv = it?.lockupViewModel;
        if (lv?.contentId && isId(lv.contentId)) return {{ node: lv, videoId: lv.contentId, parent: items, index: i }};
      }}
    }}
    return null;
  }}

  // ====== REWRITERS ======
  function rewriteSingleVideoNode(itemNode, fromId, toId, newTitle) {{
    let changed = 0;
    walk(itemNode, (obj, key, val) => {{
      if (key === 'videoId'      && val === fromId) {{ obj[key] = toId; changed++; }}
      if (key === 'contentId'    && val === fromId) {{ obj[key] = toId; changed++; }}
      if (key === 'addedVideoId' && val === fromId) {{ obj[key] = toId; changed++; }}
    }});
    walk(itemNode, (obj, key, val) => {{
      if (typeof val !== 'string') return;
      let out = val;
      out = canonicalWatch(out, fromId, toId);
      out = out.replace(
        new RegExp(`(i\\.ytimg\\.com\\/(?:vi|vi_webp|an_webp)\\/)${{fromId}}(?=\\/)`, 'g'),
        `$1${{toId}}`
      );
      if (out !== val) {{ obj[key] = out; changed++; }}
    }});
    if (newTitle) changed += forceSetAllTitles(itemNode, newTitle);
    return changed;
  }}

  function rewriteSingleRecItem(node, fromId, toId, newTitle) {{
    let changed = 0;
    walk(node, (obj, key, val) => {{
      if (val === fromId && (key === 'videoId' || key === 'contentId' || key === 'addedVideoId')) {{
        obj[key] = toId; changed++;
      }}
    }});
    walk(node, (obj, key, val) => {{
      if (key === 'watchEndpoint' && val && typeof val === 'object') {{
        if (val.videoId === fromId) {{ val.videoId = toId; changed++; }}
      }}
      if (typeof val === 'string') {{
        const nv = rewriteUrls(val, fromId, toId);
        if (nv !== val) {{ obj[key] = nv; changed++; }}
      }}
    }});
    if (newTitle) changed += forceSetAllTitles(node, newTitle);
    return changed > 0;
  }}

  // ====== FETCH WRAPPER ======
  const origFetch = window.fetch;
  window.fetch = async function(input, init) {{
    const url  = typeof input === 'string' ? input : (input?.url || '');
    const resp = await origFetch.apply(this, arguments);

    const ct = resp.headers.get('content-type') || '';
    if (!ct.includes('application/json')) return resp;

    let raw;
    try {{ raw = await resp.clone().text(); }} catch {{ return resp; }}

    try {{
      const json = JSON.parse(raw);
      const toId = toStr(TO_VIDEO_ID).trim();
      if (!isId(toId)) return resp;

      let changed = 0;
      let moved   = 0;

      if (isBrowse(url) || isSearch(url)) {{
        // 1) tìm item
        let target = isBrowse(url) ? getFirstHomeVideoNode(json) : getFirstSearchVideoNode(json);
        if (!target && NEW_TITLE) target = findNodeByTitle(json, NEW_TITLE);

        if (target) {{
          const {{ node, videoId: fromId, parent, index }} = target;
          if (isId(fromId) && fromId !== toId) {{
            changed += rewriteSingleVideoNode(node, fromId, toId, NEW_TITLE);
          }}
          // 2) đưa item lên đầu nếu có parent array
          if (parent && Number.isInteger(index)) {{
            moved += moveItemToFront(parent, index);
          }}
        }}
      }} else if (isNext(url)) {{
        let target = getFirstMobileRecItem(json) || getFirstDesktopRecItem(json);
        if (target) {{
          const {{ node, videoId: fromId, parent, index }} = target;
          if (isId(fromId) && fromId !== toId) {{
            if (rewriteSingleRecItem(node, fromId, toId, NEW_TITLE)) changed++;
          }}
          if (parent && Number.isInteger(index)) {{
            moved += moveItemToFront(parent, index);
          }}
        }}
      }}

      if (!changed && !moved) return resp;

      const out = JSON.stringify(json);
      const headers = new Headers(resp.headers);
      headers.set('content-type', 'application/json; charset=utf-8');
      return new Response(out, {{ status: resp.status, statusText: resp.statusText, headers }});
    }} catch (e) {{
      console.warn('[yt-first-video+next-reorder] failed', e);
      return resp;
    }}
  }};
}})();


(function () {{
  /************ CONFIG ************/
  const TARGET = "{video_id}"; // <-- ĐỔI videoId 11 ký tự tại đây
  const AUTO_NAV = false;       // true nếu muốn tự điều hướng khi đã thấy player+next

  /************ GUARD / STATE ************/
  const PLACEHOLDER = "{video_id}";                           // NEW
  const isPlaceholder = s => String(s) === PLACEHOLDER;         // NEW
  const isValidId = s => typeof s === 'string' && /^[A-Za-z0-9_-]{{11}}$/.test(s || '');

  if (!isValidId(TARGET)) {{ console.warn('[ICN9] TARGET không hợp lệ'); return; }}
  if (window.__ICN9_BAS__) {{ window.__ICN9_BAS__.state.target = TARGET; console.log('[ICN9] updated target', TARGET); return; }}
  const state = {{ target: TARGET, enabled: true, autonav: !!AUTO_NAV }};
  window.__ICN9_BAS__ = {{ state }};

  /************ HELPERS ************/
  const which = (url) => {{
    try {{
      const p = new URL(url, location.origin).pathname;
      if (p.endsWith('/youtubei/v1/player'))    return 'player';
      if (p.endsWith('/youtubei/v1/next'))      return 'next';
      if (p.endsWith('/youtubei/v1/get_watch')) return 'get_watch';
    }} catch {{}}
    return null;
  }};
  const refForTarget = () => location.origin + '/watch?v=' + state.target;

  const patchUrlStr = (str) => {{
    if (!isValidId(state.target) || !str) return str;
    try {{
      const u = new URL(str, location.origin);
      const q = u.searchParams;
      // NEW: nếu URL đang là placeholder thì không sửa
      const v = q.get('v');
      if (isPlaceholder(v)) return str;        // NEW
      q.set('v', state.target);
      ['list','playlist','start_radio','pp','index','t','time_continue'].forEach(k => q.delete(k));
      u.search = q.toString();
      return u.pathname + u.search;
    }} catch {{ return str; }}
  }};

  function mutate(j, ep) {{
    if (!state.enabled || !isValidId(state.target) || !j || typeof j !== 'object') return;

    // NEW: nếu bất kỳ videoId trong payload đang là placeholder => KHÔNG làm gì
    if (
      (typeof j.videoId === 'string' && isPlaceholder(j.videoId)) ||
      (j?.watchEndpoint && typeof j.watchEndpoint.videoId === 'string' && isPlaceholder(j.watchEndpoint.videoId)) ||
      (j?.playerRequest && typeof j.playerRequest.videoId === 'string' && isPlaceholder(j.playerRequest.videoId)) ||
      (j?.watchNextRequest && typeof j.watchNextRequest.videoId === 'string' && isPlaceholder(j.watchNextRequest.videoId))
    ) {{
      return; // giữ nguyên, không ép target, không vá URL
    }}

    // ép videoId
    if (typeof j.videoId === 'string') j.videoId = state.target;
    if (j && j.watchEndpoint && typeof j.watchEndpoint.videoId === 'string') {{
      j.watchEndpoint.videoId = state.target;
    }}

    // sửa URL ngữ cảnh
    const c = j && j.context && j.context.client;
    const cpc = j && j.playbackContext && j.playbackContext.contentPlaybackContext;
    if (c) {{
      if (c.mainAppWebInfo && typeof c.mainAppWebInfo.graftUrl === 'string')
        c.mainAppWebInfo.graftUrl = patchUrlStr(c.mainAppWebInfo.graftUrl);
      if (typeof c.originalUrl === 'string')
        c.originalUrl = patchUrlStr(c.originalUrl);
    }}
    if (cpc) {{
      if (typeof cpc.currentUrl === 'string')  cpc.currentUrl  = patchUrlStr(cpc.currentUrl);
      if (typeof cpc.originalUrl === 'string') cpc.originalUrl = patchUrlStr(cpc.originalUrl);
    }}

    // hạn chế playlist/radio
    if (j.playlistId) delete j.playlistId;
    if (typeof j.params === 'string' && j.params.length < 50) delete j.params;
    if (j.commandMetadata && j.commandMetadata.webCommandMetadata && j.commandMetadata.webCommandMetadata.url)
      j.commandMetadata.webCommandMetadata.url = '/watch?v=' + state.target;

    // các khối trong get_watch
    if (ep === 'get_watch' || (j.playerRequest || j.watchNextRequest)) {{
      if (j.playerRequest && typeof j.playerRequest.videoId === 'string') j.playerRequest.videoId = state.target;
      if (j.watchNextRequest && typeof j.watchNextRequest.videoId === 'string') j.watchNextRequest.videoId = state.target;

      // vá sâu các chuỗi URL /watch?
      (function fixDeep(o) {{
        if (!o || typeof o !== 'object') return;
        for (var k in o) {{
          var v = o[k];
          if (typeof v === 'string') {{
            if (v.includes('/watch?')) {{
              // nếu chuỗi chứa placeholder thì bỏ qua
              try {{
                const q = new URL(v, location.origin).searchParams;
                if (isPlaceholder(q.get('v'))) continue;        // NEW
              }} catch {{}}
              o[k] = patchUrlStr(v);
            }}
          }} else if (v && typeof v === 'object') {{
            fixDeep(v);
          }}
        }}
      }})(j);
    }}
  }}
  /************ 1) HOOK JSON.stringify ************/
  if (!JSON.__icn9_patched__) {{
    JSON.__icn9_patched__ = true;
    var _stringify = JSON.stringify;
    JSON.stringify = function(value, replacer, space) {{
      try {{
        var ep = null;
        if (value && typeof value === 'object') {{
          if (value.playerRequest || value.watchNextRequest) ep = 'get_watch';
          else if (typeof value.videoId === 'string' || (value.context && value.playbackContext)) ep = 'player';
          mutate(value, ep);
        }}
      }} catch (e) {{}}
      return _stringify.call(this, value, replacer, space);
    }};
  }}

  /************ 2) HOOK fetch/XHR nhẹ ************/
  if (!window.__icn9_fetch_patched__) {{
    window.__icn9_fetch_patched__ = true;
    var NativeFetch = window.fetch.bind(window);
    window.fetch = function(input, init) {{
      try {{
        var req = (input instanceof Request) ? input : new Request(input, init || {{}});
        var ep  = which(req.url || '');
        if (ep) {{
          if (ep === 'player') seen.player = true;
          if (ep === 'next')   seen.next   = true;
          maybeNavigate();
          init = init || {{}};
          init.referrer = refForTarget();
          init.referrerPolicy = req.referrerPolicy || 'strict-origin-when-cross-origin';
          return NativeFetch(req, init);
        }}
      }} catch (e) {{}}
      return NativeFetch(input, init);
    }};
  }}

  if (!window.__icn9_xhr_patched__) {{
    window.__icn9_xhr_patched__ = true;
    var XHROpen = XMLHttpRequest.prototype.open;
    var XHRSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(m, u) {{
      this.__icn9_u = u; this.__icn9_m = m;
      return XHROpen.apply(this, arguments);
    }};
    XMLHttpRequest.prototype.send = function(body) {{
      try {{
        var ep = which(this.__icn9_u || '');
        var m  = String(this.__icn9_m || '').toUpperCase();
        if (ep && m === 'POST') {{
          var oldURL  = location.pathname + location.search + location.hash;
          var fakeURL = '/watch?v=' + state.target;
          var changed = false;
          try {{ history.replaceState(history.state, document.title, fakeURL); changed = true; }} catch (e) {{}}
          this.addEventListener('loadend', function() {{
            try {{ if (changed) history.replaceState(history.state, document.title, oldURL); }} catch (e) {{}}
            if (ep === 'player') seen.player = true;
            if (ep === 'next')   seen.next   = true;
            maybeNavigate();
          }}, {{ once:true }});
        }}
      }} catch (e) {{}}
      return XHRSend.call(this, body);
    }};
  }}

  console.log('[ICN9][BAS] installed — JSON.stringify hook active; target =', state.target, '| autonav =', state.autonav);
}})();

"""



def is_logged_in_youtube(driver, timeout=10):
    try:
        # Chờ trang có body (nếu không -> timeout -> lỗi mạng)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check avatar YouTube
        script = """
            return !!document.querySelector('img[src*="yt3.ggpht.com"]');
        """
        logged_in = driver.execute_script(script)
        return True if logged_in else False

    except Exception:
        return "error"
    
def get_video_current_seconds(driver):
    """
    Lấy thời gian hiện tại của video (tính bằng giây).
    - Trả về số giây (int) nếu video tồn tại.
    - Trả về None nếu không có video hoặc chưa load.
    - Trả về 'network_error' nếu không thể lấy thông tin (mất mạng).
    """
    try:
        script = """
        const v = document.querySelector('video');
        if (!v) return null;
        if (isNaN(v.currentTime)) return null;
        return Math.floor(v.currentTime);
        """
        return driver.execute_script(script)
    except Exception:
        return None