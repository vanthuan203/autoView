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
        WaitElement(driver, '//input[contains(@class,"gLFyf gsfi")]', 3)
    # đồng ý Cookike:
    sleep(3)
    checkcookie = driver.find_elements(
        By.XPATH, '//button[contains(@data-ved,"0ahUK") and contains(@id,"AGLb")]')
    if (checkcookie):
        checkcookie[0].click()
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
        js_script = """
                let anchors = Array.from(document.querySelectorAll('a'));
                let videoIds = anchors
                    .map(a => a.href)
                    .filter(href => href.includes('/watch?v='))
                    .map(href => {
                        let match = href.match(/v=([\\w-]{11})/);
                        return match ? match[1] : null;
                    })
                    .filter(id => id);
                return [...new Set(videoIds)]; // loại bỏ trùng
            """

        video_ids = driver.execute_script(js_script)    
        return random.choice(video_ids) if video_ids else None
    except:
        return None

