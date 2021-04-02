#2
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('User-Agent: Mozilla/5.0 (Macintosh; M1 OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36') 

driver = webdriver.Chrome("/Users/chuseungmin/Desktop/chdrv/chromedriver", options=options)
driver.implicitly_wait(2)

#3
learningx = 'https://ocs.cau.ac.kr/index.php?module=xn_commonsi&act=dispXn_commonsiMobileLogin&return_url=https%3A%2F%2Focs.cau.ac.kr%2Findex.php%3Fmodule%3Dxn_sso2013%26act%3DprocXn_sso2013ExternalLoginCallback%26return_url%3Dhttps%253A%252F%252Feclass3.cau.ac.kr%252F%252Flearningx%252Flogin%26from%3Dweb_redirect%26login_type%3Dsso%26sso_only%3Dtrue&auto_login=true&sso_only=true&cvs_lgn='
driver.get(learningx)

cauid = input("아이디를 입력해 주세요")
caupassword = input("비밀번호를 입력해 주세요")

driver.find_element_by_id('login_user_id').send_keys(cauid)
driver.find_element_by_id('login_user_password').send_keys(caupassword)

#로그인 하기(로그인 버튼 누르기)
try:
    driver.find_element_by_xpath("""//*[@id="login_wapper"]/div[1]/div[4]/a""").click()
except:
    alert = driver.switch_to.alert
    alert.accept()
    print('Alert Occurred')
    pass

try:
    driver.find_element_by_class_name('login_box').click()
except:
    driver.get("https://eclass3.cau.ac.kr/")
    driver.find_element_by_class_name('login_box').click()
    pass


#5
#Subject Name List
subname = driver.find_element_by_xpath('//*[@id="DashboardCard_Container"]/div')
subname = subname.find_elements_by_class_name("ic-DashboardCard")
subnamelst = list()
for n in subname:
    subnamelst.append(n.get_attribute("aria-label"))
print("과목의 이름 리스트")
print(subnamelst)

#Subject Number List
subnum = driver.find_element_by_xpath('//*[@id="DashboardCard_Container"]/div')
subnum = subnum.find_elements_by_class_name('ic-DashboardCard')
subnumlst = list()
for n in subnum:
    subnumlst.append(n.get_attribute("data-reactid")[4:])
print("과목의 고유번호 리스트")
print(subnumlst, '\n\n')

#Subject Dictionary

subdic = dict(zip(subnamelst, subnumlst))
print("과목의 이름 및 고유번호 딕셔너리")
print(subdic, '\n\n')


#6
asslinklst = list()
for val in subdic.values():
    asslinklst.append("https://eclass3.cau.ac.kr/courses/"+val+"/assignments")
    

az = [1, 2, 3, 4, 5]
chuseungmin = list()
ohinwoong = list()
leesunmin = list()
for linkx in asslinklst:
    #driver.get(linkx)
    driver.get(linkx)
    try:
        try:
            element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='assignment_group_upcoming']"))
            )
        except:
            pass

        try:
            smile = driver.find_element_by_xpath('//*[@id="assignment_group_upcoming_assignments"]')
        except:
            pass
       
        try:
            for n in az:
                try:
                    xpathis = "//ul/li["+str(n)+"]/div/div/div[2]/div/div[2]/span[1]"
                    smile = smile.find_element_by_xpath(xpathis).text
                    ohinwoong.append(smile)
                except:
                    pass
        except:
            pass        
        chuseungmin.append(ohinwoong)
        ohinwoong = list()
    except:
        pass
    
for n in chuseungmin:
    if len(n)>0:
        leesunmin.append(n[0])
    else:
        leesunmin.append('')

print("(과목당) 과제의 제일 급한 숙제 모음 리스트")

inser = list(range(len(leesunmin)))
for i in inser:
    if len(leesunmin[i]) < 13:
        leesunmin[i] = "없습니다"
print(leesunmin)


subsubdic = dict(zip(subnamelst, leesunmin))
print("과목명 및 과제 중 제일 급한 숙제 딕셔너리")
print(subsubdic, '\n\n')

driver.quit()