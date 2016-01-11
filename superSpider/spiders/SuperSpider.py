import scrapy
from bs4 import BeautifulSoup
from superSpider.items import SuperspiderItem
from scrapy.http.cookies import CookieJar
import re
import urllib, urllib2, cookielib

#http://edoli.tistory.com/46 // urllib cookie example
class SuperSpider (scrapy.Spider):
    name = "super"
    allowed_domains = ["www.ggi.co.kr"]
    base_url = "https://www.ggi.co.kr"
    start_urls = ["https://www.ggi.co.kr/home1.asp"]
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    params = urllib.urlencode({'resid':'gusco7880', 'respass':'gusco7880'})


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

            yield scrapy.FormRequest(url = "https://www.ggi.co.kr/search/sojae_search.asp",
                                     formdata={
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
                                            'resResultdate':'2016-01-11',
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
                                     },
                                     method='GET',
                                     callback=self.parse_auction)

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
        print response.body
        filenmae = 'test.html'
        with open(filenmae, 'wb') as f:
            f.write(response.body)


    # continue scraping with authenticated session...



# class SuperSpider (scrapy.Spider):
#     name = "super"
#     allowed_domains = ["dmoz.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]
#
#     def parse(self, response): #call back function~
#         # filename = response.url.split("/")[-2] + '.html'
#         # with open(filename, 'wb') as f:
#         #     f.write(response.body)
#         return [FormRequest]
#
#
#         # print response.url.split("/")[0]; #http:
#         # print response.url.split("/")[-1]; #
#         # print response.url.split("/")[-2]; #Books  Resources
