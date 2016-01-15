# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from superSpider.items import SuperspiderItem
from scrapy.http.cookies import CookieJar
import re
import ssl
import cookielib
import sys,time,urllib, urllib2, os, socket,random
import chardet

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import xlsxwriter
import time



reload(sys)
sys.setdefaultencoding('utf-8')

#http://edoli.tistory.com/46 // urllib cookie example
class SuperSpider (scrapy.Spider):
    name = "super"
    allowed_domains = ["www.ggi.co.kr"]
    base_url = "http://www.ggi.co.kr"
    start_urls = ["https://www.ggi.co.kr/home1.asp"]

    cookie = ""


    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    params = urllib.urlencode({'back_url':'/home1.asp',
                               'back_string':'',
                               'resid':'gusco7880',
                               'respass':'gusco7880'})
    now = time.localtime()
    nowYear = str(now.tm_year)
    nowMonth = str(now.tm_mon)
    nowDay = str(now.tm_mday)
    nowFormalMonth =""
    nowFormalDay =""
    if(len(nowMonth)==1):
        nowFormalMonth = "0"+str(now.tm_mon)
    if(len(nowDay)==1):
        nowFormalDay = "0"+str(now.tm_mday)

    totalTime = nowYear+"-"+nowFormalMonth+"-"+nowFormalDay

    def parse(self, response): #call back function~
        print response.url
        return scrapy.FormRequest.from_response(
            response,
            formdata={'resid':'gusco7880', 'respass':'gusco7880'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            print "error.....T_T"
            return
        else:
            self.log("Login Succeed!!")
            print "Succeed!!!"
            print response.url


            req = urllib2.Request("http://www.ggi.co.kr/login/ggi_login.asp", self.params)
            res = self.opener.open(req)


            self.cookie = res.headers.get('Set-Cookie')
           # print self.cookie


            req2 = urllib2.Request("http://www.ggi.co.kr/member/my_today.asp")
            req2.add_header('cookie', self.cookie)
            res2 = self.opener.open(req2)
            #print res2.headers.get('Set-Cookie') #Note!! even though it shows None -> it works.. I can't explain it however I guess visiting my_today.asp is keypoint to get cookies
            #self.cookie = res2.headers.get('Set-Cookie')
            #print self.cookie



            formdata=urllib.urlencode({
                                            'groupresult':'',
                                            'resChgPage':'1',
                                            'nowpge':'',
                                            'choice':'1',
                                            'seqno_no':'',
                                            'popgugun':'',
                                            'popemdong':'',
                                            'search_save':'Y',
                                            'save_seq':'',
                                            'resultchk':'N',
                                            'SDay':'2',
                                            'resResultdate':self.totalTime,
                                            'AreaSelect':'1',
                                            'resSiDo':'00',
                                            'resSiGuGun':'',
                                            'resEMDong':'',
                                            'resRi':'',
                                            'addr':'',
                                            'l_addr1':'',
                                            'l_addr2':'',
                                            'resTotGamAmt1':'',
                                            'resTotGamAmt2':'',
                                            'resTotLowestAmt1':'',
                                            'resTotLowestAmt2':'',
                                            'reslandArea1':'',
                                            'reslandArea2':'',
                                            'pyung':'',
                                            'resjicheung':'ji_all',
                                            'resbuilArea1':'',
                                            'resbuilArea2':'',
                                            'bdname':'',
                                            'resYongNm':'',
                                            'resBuildYear1':'',
                                            'resBuildYear2':'',
                                            'resAuctionResult':'',
                                            'resAuctionResult2':'',
                                            'resYouchalCnt1':'',
                                            'resYouchalCnt2':'',
                                            'resjugam1':'',
                                            'resjugam2':'',
                                            'kyungGubun':'',
                                            'resSort1':'',
                                            'pgesize':'20',
                                            'Newuse':'',
                                            'useall':'',
                                            'resuse':'',
                                            'use_inc':'',
                                            'ListGubun':'',
                                            'matchchk':'',
                                            'matchname':'',
                                            'matchCount':'0',
                                            'mathchreset':'N',
                                            'reg_mgroup':''
                                     })

            req = urllib2.Request("http://www.ggi.co.kr/search/sojae_search.asp", formdata)
            req.add_header('cookie',self.cookie)
            res = self.opener.open(req)
           # print res.headers.get('Set-Cookie')
#            print self.cookie

            searchResultHtml = res.read()

            soup = BeautifulSoup(searchResultHtml,"html5lib")
            parsingNumOfTotalPage = soup.select('#noprint > td.text_Align_center')[0].get_text(strip=True).split(' P')[0].split('(')[1]
            print parsingNumOfTotalPage
            NumOfTotalPage = int(re.search(r'\d+', parsingNumOfTotalPage).group())
            print NumOfTotalPage



           # Create an new Excel file and add a worksheet.
            workbook = xlsxwriter.Workbook('demo.xlsx')
            worksheet = workbook.add_worksheet()

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.set_column('C:C', 40)

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})

            # Write some simple text.
            #worksheet.write('A1', 'Hello')

            # Text with formatting.
            #worksheet.write('A2', 'World', bold)

            #res 2 is after 14 days check
            for pageNo in range(1,NumOfTotalPage+1):
                formdata = urllib.urlencode({
                                                "search_save":"",
                                                "resSiDo":"0",
                                                "resSiGuGun":"",
                                                "resEMDong":"",
                                                "resYear1":self.nowYear,
                                                "resMonth1":self.nowMonth,
                                                "resday1":self.nowDay,
                                                "resYear2":"2016",
                                                "resMonth2":"1",
                                                "resday2":"29",
                                                "resTotGamAmt1":"",
                                                "resTotGamAmt2":"",
                                                "resTotLowestAmt1":"",
                                                "resTotLowestAmt2":"",
                                                "resLowAmtRatio":"",
                                                "resYouchalCnt1":"",
                                                "resYouchalCnt2":"",
                                                "resAuctionResult":"",
                                                "resUse":"",
                                                "useall":"",
                                                "addr":"",
                                                "resRi":"",
                                                "TodayNew":"",
                                                "TodayNewStr":"",
                                                "title_code":"",
                                                "ListGubun":"1",
                                                "resright":"",
                                                "resright2":"",
                                                "pyung":"",
                                                "resBubwon":"",
                                                "resGae":"",
                                                "AreaSelect":"1",
                                                "sday":"2",
                                                "Ex":"",
                                                "resChgPage":"1",
                                                "nowpge":pageNo,
                                                "resYongNm":"",
                                                "resBuildYear1":"",
                                                "resBuildYear2":"",
                                                "bdname":"",
                                                "reslandArea1":"",
                                                "reslandArea2":"",
                                                "resbuilArea1":"",
                                                "resbuilArea2":"",
                                                "gummulipchal":"",
                                                "tojiipchal":"",
                                                "sunimcha":"",
                                                "daejidung":"",
                                                "kyungGubun":"",
                                                "resjicheung":"ji_all",
                                                "Gubun":"",
                                                "dajung":"",
                                                "selectuse":"",
                                                "m_group":"",
                                                "mathchreset":"N",
                                                "popgugun":"",
                                                "popemdong":"",
                                                "resAuctionResult2":"",
                                                "resResultYear":"",
                                                "resResultMonth":"",
                                                "resResultDay":"",
                                                "resultchk":"N",
                                                "jigu_type":"",
                                                "r_resSiDo":"",
                                                "r_resSiGuGun":"",
                                                "roadnm":"",
                                                "gunno":"",
                                                "jiguchk":"",
                                                "choice":"1",
                                                "UseCd":"",
                                                "restotdate1":"",
                                                "restotdate2":"",
                                                "use_inc":"",
                                                "resResultdate":"42384",
                                                "resjugam1":"",
                                                "resjugam2":"",
                                                "resSort2":"startdate_asc",
                                                "pgesize":"20"
                                                })

                #change the way writing excel files
                #make way to stop terminal!

                links = Selector(text=searchResultHtml).xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()
                links = list(set(links)) #remove duplicated data
                sizeOfLinks = len(links)

                for index, link in enumerate(links):
                    links[index] = link.replace("..",self.base_url)
                    #print links[index]



                itemsList = []

                for linkIdx, link in enumerate(links):
                    req = urllib2.Request(link)
                    res = self.opener.open(req)
                    print res.url

                    rawdata = res.read()
                    encoding = chardet.detect(rawdata)
                    html = rawdata.decode(encoding['encoding'])

           # links = response.xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()
                  #  print Selector(text=html).css('td[class="td1"]').extract()

        #http://www.dreamy.pe.kr/zbxe/CodeClip/163260
        #http://www.yangbeom.link/post/130613532096/python%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%ED%81%B4%EB%A6%AC%EC%95%99-%ED%8C%8C%EC%84%9C%EB%A7%8C%EB%93%A4%EA%B8%B0-beautifulsoup-%EC%82%AC%EC%9A%A9%ED%8E%B8

                    print "=======Beautiful soup Parsing HTML "+str(linkIdx)+"/"+str(sizeOfLinks)+"======"
                    soup = BeautifulSoup(html,"html5lib") #you have install it with "pip install html5lib"
                   # find_mytr = soup.find_all("tr", attrs={'class':"td_1"})
                  #  print soup
                    #print soup.title.get_text().encode('cp949','ignore') # refer from https://kldp.org/node/81708
                    #itemLocNo = soup.title.get_text().encode('cp949','ignore').split()[0]
                    itemLocNo = soup.title.get_text().split()[0]
                    print soup.title.get_text().encode('cp949','ignore')
                   # print soup.find_all(id="Table1")
                    #print soup.find_all("td", class_="td_1")
                    #print soup.select("#Table1 > tbody")
                    #print soup.select("#Table1 > tbody > tr")
                    #print soup.select("#Table1 > tbody > tr + tr")
                    #print soup.select("#Table1 > tbody > tr + tr > td")
                    #print soup.select('td[class="td_1"]')  # I find it!!
                    tdList = soup.select('td[class="td_1"]')
                #    for td in tdList:
                #        print td.get_text(strip=True).encode('cp949','ignore')
                    #itemLocation = tdList[0].get_text(strip=True).encode('cp949','ignore')
                    #itemName = tdList[4].get_text(strip=True).encode('cp949','ignore')
                    itemLocation = tdList[0].get_text(strip=True)
                    itemName = tdList[4].get_text(strip=True)
                    itemExpectedPrice = tdList[6].get_text(strip=True)
                    itemMinPrice = tdList[9].get_text(strip=True)
                    itemPrice = itemExpectedPrice+"<br style='mso-data-placement:same-cell;'> "+itemMinPrice
                    #print itemName
                    #print itemLocNo
                    #print itemLocation
                    items = [itemName, itemLocNo, itemLocation, itemPrice]

                    itemsList.append(items)




                # Write some numbers, with row/column notation.

                for rowidx, items in enumerate(itemsList):
                    for colindx, item in enumerate(items):
                        worksheet.write(rowidx, colindx, item)

                if(False):
                    workbook.close() #page End if button will be clicked , I have to make it

            workbook.close() #page Final End
            #workbook 닫는 타이밍
            #사건번호 정규식 및 엔터
            #Python regex test web   regexr.com






                    #print soup.select("#Table1 > tbody > tr + tr > td.td_1")
                    #//*[@id="Table1"]/tbody/tr[1]/td[2]
                    ##Table1 > tbody > tr:nth-child(1) > td.td_1  ## error reason : http://stackoverflow.com/questions/24720442/selecting-second-child-in-beautiful-soup-with-soup-select

                    #print find_mytr
                    #for t in find_mytr:
                    #    print t.get_text(strip=True).encode('cp949','ignore').decode('cp949')

                 #   filenmae = 'test.html'
                 #   with open(filenmae, 'wb') as f:
                 #       f.write(html)




