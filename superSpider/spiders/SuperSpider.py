import scrapy
from bs4 import BeautifulSoup
from superSpider.items import SuperspiderItem
from scrapy.http.cookies import CookieJar
import re
import ssl
import cookielib
import sys,time,urllib, urllib2, os, socket,random
import chardet
from lxml import etree
import StringIO
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

reload(sys)
sys.setdefaultencoding('utf-8')

#http://edoli.tistory.com/46 // urllib cookie example
class SuperSpider (scrapy.Spider):
    name = "super"
    allowed_domains = ["www.ggi.co.kr"]
    base_url = "https://www.ggi.co.kr"
    start_urls = ["https://www.ggi.co.kr/home1.asp"]

    cookie = ""


    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    params = urllib.urlencode({'back_url':'/home1.asp',
                               'back_string':'',
                               'resid':'gusco7880',
                               'respass':'gusco7880'})



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
            print res2.headers.get('Set-Cookie') #Note!! even though it shows None -> it works.. I can't explain it however I guess visiting my_today.asp is keypoint to get cookies
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
                                            'resResultdate':'2016-01-12',
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


            req = urllib2.Request("http://www.ggi.co.kr/common/mulgun_detail_popup2.asp?idcode=A1423E403E3E3F3E3D483E3D3F43473F483E3C6&resStartDate=20160113&new=new")
            res = self.opener.open(req)
            print res.url
            #print res.read()




            rawdata = res.read()
            encoding = chardet.detect(rawdata)
            html = rawdata.decode(encoding['encoding'])

   # links = response.xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()
            print Selector(text=html).css('td[class="td1"]').extract()

#http://www.dreamy.pe.kr/zbxe/CodeClip/163260
#http://www.yangbeom.link/post/130613532096/python%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%ED%81%B4%EB%A6%AC%EC%95%99-%ED%8C%8C%EC%84%9C%EB%A7%8C%EB%93%A4%EA%B8%B0-beautifulsoup-%EC%82%AC%EC%9A%A9%ED%8E%B8

#            print "=======Beautiful soup Test======"
 #           soup = BeautifulSoup(html,"lxml")
  #          find_mytr = soup.find_all("tr", attrs={'class':"td_1"})
   #         print soup
    #        print soup.title
     #       print find_mytr
      #      for t in find_mytr:
       #         print t.get_text(strip=True).encode('cp949','ignore').decode('cp949')


#            print "=======lxml etree xpath Test======"
 #           #parser = etree.HTMLParser()
  #          #tree   = etree.parse(StringIO.StringIO(html), parser)
   #         tree = etree.HTML(html)
    #        print tree
     #       print tree.xpath('//*[@id="Table2"]/tbody/tr[7]/td[2]/table[2]/tbody/tr[2]/td[4]/text()[1]')



          #  filenmae = 'test.html'
          #  with open(filenmae, 'wb') as f:
          #      f.write(soup.title.get_text())





       #     filenmae = 'test.html'
       #     with open(filenmae, 'wb') as f:
       #         f.write(html)



    # https://youtu.be/fKF58sfZI5s?t=32m33s   // item
    def parse_auction(self, response):
        print "parse_auction finished"
        print response.url

       # soup = BeautifulSoup(response.body, "html.parser") #lxml
        item = SuperspiderItem()

        print "itemNo"
        links = response.xpath('//a[contains(@href, "common/mulgun_detail_popup2")]/@href').extract()

        for index, link in enumerate(links):
            links[index] = link.replace("..",self.base_url)

        print links[0]
       # urls = soup.select('a')
       # print soup
        yield scrapy.Request(url='https://www.ggi.co.kr/common/mulgun_detail_popup2.asp?idcode=A1493E473E413F3E3E3E3E3D403D42463F3E3C6&resStartDate=20160111&new=new',
                              method='GET',
                              callback=self.parse_page2)
        #check login session or cookie problem~!


    def parse_page1(self, response):
        return scrapy.Request("http://www.example.com/some_page.html",
                              callback=self.parse_page2)

    def parse_page2(self, response):
        # this would log http://www.example.com/some_page.html
        print response.url
      #  print response.body
        filenmae = 'test.html'
        with open(filenmae, 'wb') as f:
            f.write(response.body)

