"""
bu kod selenium ile otonom bir şekilde belirli bir twiter adresinden
beliirlenen twiter adresine gidilerek kaydırma işlemi ile tweetlerin 
toplanmasına dayanmaktadır

"""
#
"""
oturum kapatma
oturum kapatma olmaz ise selenium hata verir
program her çalıştığında oturumu kapatmalıyız
"""

from selenium import webdriver
from selenium.common import exceptions

try:
    session = webdriver.Chrome()
    print("Current session is {}".format(session.session_id))
    session.quit()
    
    try:
        session.get("https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoidHIifQ%3D%3D%22%7D")
    except exceptions.InvalidSessionIdException as e:
        print(e.message)
except:
    print("oturum kapatılamadı")
#
"""
burada hangi hesaptan gireceğimizi belirliyoruz 
girişlerde twiter karşımıza farklı olasılıklar çıkardağı
için her ihtimali göz önünde bulundurmalıyız
"""
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import pandas as pd
#path:kullanıcağımız tarayıcın driver ını indirip yolunu buraya yazıyoruz
path="C:\\Users\\Selman\\Desktop\\chromedriver"
browser=webdriver.Chrome(path)
browser.get("https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoidHIifQ%3D%3D%22%7D")
time.sleep(7)
emailbutton=browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
#giriş yapılacak mail
emailbutton.send_keys("ahmetmehmet2229@gmail.com")
time.sleep(7)
emailbutton.send_keys(Keys.ENTER)
time.sleep(7)
#ihtimallere karşı try except yapısını kullanıyoruz
try:
    sifre_alanı=browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
    sifre_alanı.send_keys("a2229Myzl")
    sifre_alanı.send_keys(Keys.ENTER)
except:
    time.sleep(7)
    kullanıcı_adı=browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
    kullanıcı_adı.send_keys("ahmetmehmet2229")
    kullanıcı_adı.send_keys(Keys.ENTER)
    time.sleep(7)
    new_pasword_area=browser.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
    new_pasword_area.send_keys("a2229Myzl")
    new_pasword_area.send_keys(Keys.ENTER)
    time.sleep(7)
try:
    search_area=browser.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
    #aranacak kişinin hesap ismi
    search_area.send_keys("elonmusk")
    search_area.send_keys(Keys.ENTER)
    time.sleep(11)
    people_button=browser.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div")
    people_button.click()
    time.sleep(10)
except:
    browser.close()
    print("tanımlanamayan bubble oluştu lütfen tekrar çalıştırın")    
    
#burdan sonra tweetleriçekmeye gidiyoruz
searc_people_button=browser.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[1]/div/div/div/div/div[2]")
searc_people_button.click()
time.sleep(8)

#scroll sayısı belirleme
"""
aşağıda ki while döngüsünün a değeri
kaç defa aşağı kaydırma yapılacağını belirtir

"""

#verilerin düzenli olabilmesi için pandas ile dataframe oluşturarak kayıt işlemi yapacığız
#verileri tutmak için 2 tane liste oluşturuyoruz
tweet_listesi=[]
tweet_tarihleril=[]
a=0

while a<45:
    sayfa_kaynagi=browser.page_source
    soup=BeautifulSoup(sayfa_kaynagi,"lxml")
    i=2
    
    #parçalama
    tweetler=soup.find_all("div",attrs={"data-testid":"cellInnerDiv"})
    
    for i in tweetler:
        #böyle yazmazsak text hatası veriyor
        try:
            tweetleri=i.find("div",attrs={"data-testid":"tweetText"})
            tweet_zamanı=i.find("time")
            
            #boş tweetleri almıyoruz
            if "None" in tweetleri.string:
                pass
            
            atilan_tweetler=str(tweetleri.string)
            tweetler_tarihi=str(tweet_zamanı.text)
            print(atilan_tweetler)
            print("    ")
            print("tarih "+tweetler_tarihi)
            print("*************************")
            #daha sonra data framelemek için listeliyoruz
            tweet_listesi.append(atilan_tweetler)
            tweet_tarihleril.append(tweetler_tarihi)
            #
        except:
           pass
    #bir kere scroll yapma kodu   
    #scroll
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    i=0
    while i<1:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        newHeight = browser.execute_script("return document.body.scrollHeight")
    
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
        i = i+1
    time.sleep(5)
    #scroll
    a=a+1
    i=i+1
browser.close()
#oturum kapanma hatası için .quit methodunu da kullanıyoruz
browser.quit()
###########################################
#kayıt işlemi
veri={"tarih":tweet_tarihleril,
      "tweetler":tweet_listesi}

df=pd.DataFrame(veri)
#dosya ismi buradan değiştirilebilir
df.to_excel("elon_musk_tweetleri_tarihleri.xlsx")
