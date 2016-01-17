# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
#from superSpider.items import SuperspiderItem
from scrapy.http.cookies import CookieJar
import re
import ssl
import cookielib
import os
import sys,time,urllib, urllib2, os, socket,random
import chardet

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import xlsxwriter


from scrapy.cmdline import execute

from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
import time
from PyQt4.QtCore import QThread

reload(sys)
sys.setdefaultencoding('utf-8')





class Form(QtGui.QDialog):

    crawl_flag=False
    nowYear=""
    nowMonth=""
    nowDay=""
    SDay=""
    resYear1=""
    resMonth1=""
    resday1=""
    resResultdate=""
    resYear2=""
    resMonth2=""
    resday2=""
    resTotGamAmt1=""
    resTotGamAmt2=""
    resYongNm=""


    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("superSpider.ui", self)

        #create a QDateTimeEdit object
        myDTE = QtGui.QDateTimeEdit()
        now = QtCore.QDateTime.currentDateTime()
        today = QtCore.QDate.currentDate()
        self.ui.resResultdate.setDate(today)
        self.ui.resResultdate2.setDate(today.addDays(14))

        self.nowYear=str(today.year())
        self.nowMonth=str(today.month())
        self.nowDay=str(today.day())
        if(len(self.nowMonth)==1):
            self.nowMonth = "0"+self.nowMonth
        if(len(self.nowDay)==1):
            self.nowDay = "0"+self.nowDay

        #print self.ui.resResultdate.date().year()
        #print self.ui.resResultdate.date().month()
        #print self.ui.resResultdate.date().day()

        self.superSpiderThread = self.SuperSpiderThread(self)
        self.connect(self.superSpiderThread, QtCore.SIGNAL("finishedWork"), self.done)
        self.connect(self.superSpiderThread, QtCore.SIGNAL("loggingWork"), self.traceLog)
        #This is about Signal and it is point https://nikolak.com/pyqt-threading-tutorial/

        self.ui.show()

    def closeEvent(self, event):
            print "User has clicked the red x on the main window"
            event.accept()

    def done(self, sigstr):
        print "SigStr~~"
        print sigstr
        self.ui.logOfProgress.setPlainText("End, Complete\n"+self.ui.logOfProgress.toPlainText()) #QObject: Cannot create children for a parent that is in a different thread.
        print "Done!" #TypeError: done() takes exactly 1 argument (2 given)

    def traceLog(self, sigLogStr):
        print "SigLogStr~~"
        print sigLogStr
        self.ui.logOfProgress.setPlainText(sigLogStr+"\n"+self.ui.logOfProgress.toPlainText()) #QObject: Cannot create children for a parent that is in a different thread.
        print "Logging!" #TypeError: done() takes exactly 1 argument (2 given)

    @pyqtSlot()
    def start_crawl(self):
        self.crawl_flag=False

        if(self.ui.SDay2.isChecked()):
            self.SDay="2"
            self.resYear1=str(self.ui.resResultdate.date().year())
            self.resMonth1=str(self.ui.resResultdate.date().month())
            self.resday1=str(self.ui.resResultdate.date().day())

            if(len(self.resMonth1)==1):
               self.resMonth1 = "0"+self.resMonth1
            if(len(self.resday1)==1):
                self.resday1 = "0"+self.resday1

            self.resResultdate = self.resYear1+"-"+self.resMonth1+"-"+self.resday1
            print self.resResultdate
            self.resYear2=""
            self.resMonth2=""
            self.resday2=""

        elif(self.ui.SDay1.isChecked()):
            self.SDay="1"
            resYear1=str(self.ui.resResultdate.date().year())
            resMonth1=str(self.ui.resResultdate.date().month())
            resday1=str(self.ui.resResultdate.date().day())

            if(len(self.resMonth1)==1):
               self.resMonth1 = "0"+self.resMonth1
            if(len(self.resday1)==1):
                self.resday1 = "0"+self.resday1

            self.resResultdate = self.resYear1+"-"+self.resMonth1+"-"+self.resday1

            self.resYear2=str(self.ui.resResultdate2.date().year())
            self.resMonth2=str(self.ui.resResultdate2.date().month())
            self.resday2=str(self.ui.resResultdate2.date().day())

            if(len(self.resMonth2)==1):
               self.resMonth2 = "0"+self.resMonth2
            if(len(self.resday2)==1):
                self.resday2 = "0"+self.resday2

        else:
            self.SDay="2"
            self.resYear1=str(self.ui.resResultdate.date().year())
            self.resMonth1=str(self.ui.resResultdate.date().month())
            self.resday1=str(self.ui.resResultdate.date().day())

            if(len(self.resMonth1)==1):
               self.resMonth1 = "0"+self.resMonth1
            if(len(self.resday1)==1):
                self.resday1 = "0"+self.resday1

            self.resResultdate = self.resYear1+"-"+self.resMonth1+"-"+self.resday1
            print self.resResultdate
            self.resYear2=""
            self.resMonth2=""
            self.resday2=""


        choices = { '0':'', '1':'0', '2':'1', '3':'3', '4':'5', '5':'7', '6':'10', '7':'15', '8':'20', '9':'25', '10':'30',
                    '11':'40', '12':'50', '13':'60', '14':'70', '15':'80', '16':'90', '17':'100', '18':'150', '19':'200', '20':'300','21':'500'}
        self.resTotGamAmt1 = choices[str(self.ui.resTotGamAmt1.currentIndex())]

        choices2 = { '0':'', '1':'0', '2':'1', '3':'3', '4':'5', '5':'7', '6':'10', '7':'15', '8':'20', '9':'25', '10':'30',
                    '11':'40', '12':'50', '13':'60', '14':'70', '15':'80', '16':'90', '17':'100', '18':'150', '19':'200', '20':'300','21':'999999'}
        self.resTotGamAmt2 = choices2[str(self.ui.resTotGamAmt2.currentIndex())]
        print self.resTotGamAmt1
        print self.resTotGamAmt2

        choices3 = {
            '0':'', '1':'A1,A2,A3,A4,A5,A6,B1,B2,B3,B4,C1,C2,C3,D1,D2,D3', '2':'A1,A2,A3,A4,A5,A6', '3':'A1', '4':'A2', '5':'A3',
        '6':'A4', '7':'A5', '8':'A6', '9':'B1,B2,B3,B4', '10':'B1', '11':'B2', '12':'B3', '13':'B4',
        '14':'C1,C2,C3', '15':'C1', '16':'C2', '17':'C3', '18':'D1,D2,D3', '19':'D1', '20':'D2', '21':'D3', '22':'E1,E2,E3',
        '23':'E1', '24':'E2', '25':'E3', "26":'F1', '27':'G1'
        }
        self.resYongNm = choices3[str(self.ui.resYongNm.currentIndex())]
        print self.resYongNm


        self.ui.logOfProgress.setPlainText("Start Downloading....\n")
        self.ui.show()

        self.superSpiderThread.start()
        #execute(['scrapy','crawl','super'])
        #self.ui.label.setText("Hello~")

    @pyqtSlot()
    def stop_crawl(self):
        self.crawl_flag=True
        #self.ui.label.setText("두번째 버튼")





#http://edoli.tistory.com/46 // urllib cookie example



    class SuperSpiderThread (QThread):



        def __init__(self, super):
            QThread.__init__(self)
            self.super = super

        def __del__(self):
            self.wait()

        def run(self):
            #your logic here

            print self.super.resYongNm
            name = "super"
            allowed_domains = ["www.ggi.co.kr"]
            base_url = "http://www.ggi.co.kr"
            start_urls = ["https://www.ggi.co.kr/home1.asp"]

            cookie = ""


            formdata=urllib.urlencode({'resid':'gusco7880', 'respass':'gusco7880'})
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            req = urllib2.Request("http://www.ggi.co.kr/home1.asp", formdata)
            res = opener.open(req)
            self.after_login(res)



        def after_login(self, response):

            base_url = "http://www.ggi.co.kr"
            cookie = ""
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            params = urllib.urlencode({'back_url':'/home1.asp',
                                       'back_string':'',
                                       'resid':'gusco7880',
                                       'respass':'gusco7880'})



            print "Succeed!!!"


            print response.url


            req = urllib2.Request("http://www.ggi.co.kr/login/ggi_login.asp", params)
            res = opener.open(req)


            cookie = res.headers.get('Set-Cookie')
           # print self.cookie


            req2 = urllib2.Request("http://www.ggi.co.kr/member/my_today.asp")
            req2.add_header('cookie', cookie)
            res2 = opener.open(req2)
            #print res2.headers.get('Set-Cookie') #Note!! even though it shows None -> it works.. I can't explain it however I guess visiting my_today.asp is keypoint to get cookies
            #self.cookie = res2.headers.get('Set-Cookie')
            #print self.cookie

            print self.super.resResultdate
            print "resTotGamAmt1 Test!!"
            print self.super.resTotGamAmt1
            print "resTotGamAmt1 End!!"

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
                                            'SDay':self.super.SDay,
                                            'resResultdate':self.super.resResultdate,
                                            'AreaSelect':'1',
                                            'resSiDo':'00',
                                            'resSiGuGun':'',
                                            'resEMDong':'',
                                            'resRi':'',
                                            'addr':'',
                                            'l_addr1':'',
                                            'l_addr2':'',
                                            'resTotGamAmt1':self.super.resTotGamAmt1,
                                            'resTotGamAmt2':self.super.resTotGamAmt2,
                                            'resTotLowestAmt1':'',
                                            'resTotLowestAmt2':'',
                                            'reslandArea1':'',
                                            'reslandArea2':'',
                                            'pyung':'',
                                            'resjicheung':'ji_all',
                                            'resbuilArea1':'',
                                            'resbuilArea2':'',
                                            'bdname':'',
                                            'resYongNm':self.super.resYongNm,
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
                                            'mathchreset':'Y',
                                            'reg_mgroup':''
                                     })
            print formdata

            req = urllib2.Request("http://www.ggi.co.kr/search/sojae_search.asp", formdata)
            req.add_header('cookie',cookie)
            res = opener.open(req)
           # print res.headers.get('Set-Cookie')
    #            print self.cookie

            searchResultHtml = res.read()

            soup = BeautifulSoup(searchResultHtml,"html5lib")
            parsingNumOfTotalPage = soup.select('#noprint > td.text_Align_center')[0].get_text(strip=True).split(' P')[0].split('(')[1]
            print parsingNumOfTotalPage
            NumOfTotalPage = int(re.search(r'\d+', parsingNumOfTotalPage).group())
            print NumOfTotalPage

            paramNumOfTotal = "Total "+str(NumOfTotalPage)+" Pages"
            self.super.ui.numOfTotal.setText(paramNumOfTotal)

            parsingNumOfTotalItems = soup.select('#noprint > td.text_Align_center')[0].get_text(strip=True).split(', ')[1]
            NumOfTotalItems = int(re.search(r'\d+', parsingNumOfTotalItems).group())

            paramNumOfTotalItems = "Total "+str(NumOfTotalItems)+" Items"
            self.super.ui.numOfTotalItems.setText(paramNumOfTotalItems)

           # Create an new Excel file and add a worksheet.
            fileName = self.super.nowYear+self.super.nowMonth+self.super.nowDay+"_"+"경매물건DB.xlsx".encode('cp949','ignore')
            workbook = xlsxwriter.Workbook(fileName)
            worksheet = workbook.add_worksheet()

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 15)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})

            # Write some simple text.
            worksheet.write('A1', '사건번호')
            worksheet.write('B1', '성명')
            worksheet.write('C1', '주소')
            worksheet.write('D1', '감정가')
            worksheet.write('E1', '최저가')
            worksheet.write('F1', '상태')

            # Text with formatting.
            #worksheet.write('A2', 'World', bold)

            #res 2 is after 14 days check

            indexOfItems = 0
            rowidx = 0
            for pageNo in range(1,NumOfTotalPage+1):
                formdata = urllib.urlencode({
                                                "search_save":"",
                                                "resSiDo":"0",
                                                "resSiGuGun":"",
                                                "resEMDong":"",
                                                "resYear1":self.super.resYear1,
                                                "resMonth1":self.super.resMonth1,
                                                "resday1":self.super.resday1,
                                                "resYear2":self.super.resYear2,
                                                "resMonth2":self.super.resMonth2,
                                                "resday2":self.super.resday2,
                                                "resTotGamAmt1":self.super.resTotGamAmt1,
                                                "resTotGamAmt2":self.super.resTotGamAmt2,
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
                                                "sday":self.super.SDay,
                                                "Ex":"",
                                                "resChgPage":"1",
                                                "nowpge":pageNo,
                                                "resYongNm":self.super.resYongNm,
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
                req = urllib2.Request("http://www.ggi.co.kr/search/sojae_search.asp", formdata)
                req.add_header('cookie',cookie)
                res = opener.open(req)
               # print res.headers.get('Set-Cookie')
        #            print self.cookie

                searchResultHtml = res.read()
#
                filenmae = 'test.html'
                with open(filenmae, 'wb') as f:
                    f.write(searchResultHtml)


#

                links = Selector(text=searchResultHtml).xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()
                links = list(set(links)) #remove duplicated data
                sizeOfLinks = len(links)

                for index, link in enumerate(links):
                    links[index] = link.replace("..",base_url)
                    #print links[index]



                itemsList = []

                for linkIdx, link in enumerate(links):
                    req = urllib2.Request(link)
                    res = opener.open(req)
                    print res.url

                    rawdata = res.read()
                    encoding = chardet.detect(rawdata)
                    html = rawdata.decode(encoding['encoding'])

                    indexOfItems = indexOfItems+1

           # links = response.xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()
                  #  print Selector(text=html).css('td[class="td1"]').extract()

        #http://www.dreamy.pe.kr/zbxe/CodeClip/163260
        #http://www.yangbeom.link/post/130613532096/python%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%ED%81%B4%EB%A6%AC%EC%95%99-%ED%8C%8C%EC%84%9C%EB%A7%8C%EB%93%A4%EA%B8%B0-beautifulsoup-%EC%82%AC%EC%9A%A9%ED%8E%B8
                    self.emit(QtCore.SIGNAL('loggingWork'), "=======Downloading and Parsing HTML files "+str(indexOfItems)+"/"+str(NumOfTotalItems)+"======")
                    print "=======Beautiful soup Parsing HTML "+str(indexOfItems)+"/"+str(NumOfTotalItems)+"======"
                   # logOfProgress.setPlainText("=======Beautiful soup Parsing HTML "+str(linkIdx+1)+"/"+str(sizeOfLinks)+"======\n")

                    soup = BeautifulSoup(html,"html5lib") #you have install it with "pip install html5lib"
                   # find_mytr = soup.find_all("tr", attrs={'class':"td_1"})
                  #  print soup
                    #print soup.title.get_text().encode('cp949','ignore') # refer from https://kldp.org/node/81708
                    #itemLocNo = soup.title.get_text().encode('cp949','ignore').split()[0]
                    itemLocNoSplited = soup.title.get_text().split()
                    itemLocNo = itemLocNoSplited[0]+" "+itemLocNoSplited[1]
                    #print soup.title.get_text().encode('cp949','ignore')
                    print soup.title.get_text()
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
                    itemLocation = tdList[0].get_text(strip=True).split('[')[0]
                    itemLocation = itemLocation.split('(')[0] #without name of road
                    itemName = tdList[4].get_text(strip=True)
                    itemExpectedPrice = tdList[6].get_text(strip=True)
                    itemMinPrice = tdList[9].get_text(strip=True)
                    #itemPrice = itemExpectedPrice+" / "+itemMinPrice
                    #print itemName
                    #print itemLocNo
                    #print itemLocation
                    items = [itemLocNo, itemName, itemLocation, itemExpectedPrice, itemMinPrice]

                    itemsList.append(items)

                    if(self.super.crawl_flag):
                        print "Close Excel File"
                        workbook.close() #page End if button will be clicked , I have to make it
                        break

                    rowidx = rowidx+1
                    for colindx, item in enumerate(items):
                        worksheet.write(rowidx, colindx, item)

                if(self.super.crawl_flag):
                    print "break outer loop"
                    break


                # Write some numbers, with row/column notation.

                #for rowidx, items in enumerate(itemsList):
                #    for colindx, item in enumerate(items):
                #        worksheet.write(rowidx+1, colindx, item)



            print "End of Loop"
            workbook.close() #page Final End
            self.emit(QtCore.SIGNAL('finishedWork'), "hi program finished from thread")

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec_())

class superSpiderThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        print ""
        #your logic here
