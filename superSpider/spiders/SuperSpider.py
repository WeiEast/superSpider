import scrapy

class SuperSpider (scrapy.Spider):
    name = "super"
    allowed_domains = ["www.ggi.co.kr"]
    start_urls = ["https://www.ggi.co.kr/home1.asp"]

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
                                            'resResultdate':'2016-01-05',
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
            # print response.body
            # problem is.. why url reset on another url

    # def search_auction(self, response):
    #     print "search~"
    #     return scrapy.FormRequest.from_response(
    #         response,
    #         formdata={'resResultdate':'2016-01-05' },
    #         callback=self.parse_auction
    #     )

    def parse_auction(self, response):
        print "parse_auction finished"
        filenmae = 'test.html'
        with open(filenmae, 'wb') as f:
            f.write(response.body)
        # print response.body


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
