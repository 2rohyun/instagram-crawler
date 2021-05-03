from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException as NOERROR
import time
import pandas as pd
import pandas_csv

# 인스타그램 태그를 입력하여 해당 태그에 대한 검색 결과 웹 페이지를 띄움.
baseUrl = 'https://www.instagram.com/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome() 
driver.get(url) 
driver.implicitly_wait(10) # 페이지가 로딩될 때 까지 암묵적으로 기다린다.

driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click() 
driver.find_element_by_name('username').send_keys("") # 본인 인스타그램 아이디 입력 
driver.find_element_by_name('password').send_keys("") # 본인 인스타그램 비밀번호 입력
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

time.sleep(3) # 로그인 대기시간

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
#driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
#driver.get(url)

post_number = 1

follower = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
follow_num = follower.text
print("number of followers : ", follow_num) # 팔로워 수 

driver.find_element_by_class_name("_9AhH0").click()

while True:
    try:
        loc = driver.find_element_by_class_name("O4GlU")
        location = loc.text
        print("location in this post : ", location) # 게시물의 위치 
        print("\n")
    except:
        location = " - "
        print("no location in this post")

    date = driver.find_element_by_class_name("_1o9PC.Nzb55")
    post_date = date.get_attribute('title')
    print("date in this post : ", post_date) # 게시물 날짜 
    
    try:
        matched_elements = driver.find_elements_by_class_name("xil3i")
        hashtags = []

        for matched_element in matched_elements:
            hashtag = matched_element.text
            hashtags.append(hashtag)
        print(hashtags) # 게시물 해시태그 

    except NOERROR:
        print("No hashtags in this post")
    
    try:
        post_write = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
        post = post_write.text
        print(post) # 게시물에 포함된 게시글 
    except NOERROR:
        post = " - "
        print("no post write in this post")

    
    try:
        likes_other = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/button/span')
        likes_num = likes_other.text
        print("number of likes : ", likes_num) # 게시물 좋아요 수 
        print("\n")  
    except NOERROR:
        try:
            likes = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button/span')
            likes_num = likes.text
            print("number of likes : ", likes_num)
            print("\n")
        except NOERROR:
            likes_num = 0
            print("this is video")
    
    insert_data = {"user id" : plusUrl,
                   "number of followers" : follow_num,
                   "post number" : post_number,
                   "likes" : likes_num,
                   "location" : location,
                   "date time" : post_date,
                   "post write" : post,
                   "hashtags" : [hashtags]}
    pandas_csv.to_csv(insert_data)
    post_number += 1
    print("게시물 번호 : ", post_number)
    try:
        nextbtn = driver.find_element_by_class_name(
            "_65Bje.coreSpriteRightPaginationArrow"
        )
        if nextbtn.text in ("다음", "Next"):
            nextbtn.click()
    except:  
        break