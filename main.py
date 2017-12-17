"""main.py: yes24의 베스트셀러 책들의 info를 가져와 data.txt파일로저장"""
__author__      = "devHyung"
__version__ = "1.0.0"
__maintainer__ = "devHyung"

import requests
from bs4 import BeautifulSoup

class Book():
    def __init__(self,soup):
        self.name = "" #책제목
        self.author = ""#책저자
        self.price = ""#판매가
        self.point = ""#yes포인트
        self.pdDate = ""#출간일
        self.saleNum = ""#판매지수
        self.setInfoBySoup(soup)
    def setInfoBySoup(self,soup):
        # ____________________책제목및 기본정보가져오기___________
        self.name = soup.find('div', id='title').find('h1').find('a').get_text() #책제목
        try:#부제가 있을수도 없을수도있다.
            subname = soup.find('div', id='title').find('span', class_='subtitle').get_text()#부제가있음
            self.name += subname
        except:#부제가없음
            pass
        self.author = soup.find('div', id='title').find('p').get_text() # 저자가져오기
        #____________________책가격및 할인율 포인트 가져오기 ___________
        tablelist = soup.find('table',summary="상품 가격정보 테이블")
        tablelist = tablelist.find_all('tr')
        self.price = tablelist[1].find('td').get_text() #판매가, 할인율 포함
        self.point = tablelist[2].find('td').get_text() #포인트
        # ____________________출간일 및 판매지수 가져오기 ___________
        self.pdDate = soup.find('dd', class_='pdDate').find('p').get_text()# 출간일
        self.saleNum = soup.find('dt', class_='saleNum').get_text().split(' ')[-2] #판매지수
    def stripAll(self):#불필요한 공백제거
        self.name = self.name.strip()
        self.author = self.author.strip()
        self.price = self.price.strip()
        self.point = self.point.strip() # '못참는아이 욱하는 아이' 도서 포인트쪽보면 마니아 추가적립이란 단어가포함
        # 그래서 이코드추가
        self.point = self.point.replace('\r', '')
        self.point = self.point.replace('\n', '')
        self.point = self.point.replace(' ', '')
        self.pdDate =  self.pdDate.strip()
        self.saleNum = self.saleNum.strip()
    def getInfoDeliBySemicol(self):# ;을 딜리미터로 책정보를 string으로 리턴
        self.stripAll()
        return  self.name+';'+self.author+';'+self.price+';'+self.point+';'+self.pdDate+';'+self.saleNum+'\n'


def getAllBookInfoByUrl(bookurllist):
    booklist = []
    progressidx = 1
    for bookurl in bookurllist:
        print ( progressidx , "개 책정보 추출중...")
        source_code = requests.get(bookurl)  # url을 기준 웹소스코드를 가져옴
        soup = BeautifulSoup(source_code.text, "lxml")  # source code를 parsing하기좋게 BeautifulSoup객체로변환
        bookdata = Book(soup) # soup객체를 주면 클래스안에서 자동적으로 추출
        booklist.append(bookdata) # book클래스를 리스트에 추가
        progressidx += 1
    with open("data.txt", "w") as f:
        for bookdata in booklist:
            f.write( bookdata.getInfoDeliBySemicol())


def getAllUrlList():
    urllist = []
    base_url = "http://www.yes24.com"
    bestseller_path = "/24/category/bestseller"
    source_code = requests.get(base_url+bestseller_path) # url을 기준 웹소스코드를 가져옴
    soup = BeautifulSoup(source_code.text,"lxml") # source code를 parsing하기좋게 BeautifulSoup객체로변환
    sellerlist = soup.find_all('p',class_="copy")
    for data in sellerlist:#bestseller list를 돌면서 a태그 안의 href를 추출 urllist에 저장
        urllist.append(base_url+data.find('a').get('href'))
    return urllist

if __name__ == "__main__":
    urllist = getAllUrlList() # bestseller 책들의 각각의 url들을 가져온다
    getAllBookInfoByUrl(urllist)

