import scrapy
from healthboards.items import HealthboardsItem

class HBSpider(scrapy.Spider):
    name = "healthb"

    def start_requests(self):
        urls = [
            'https://www.healthboards.com/boards',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_boards)

    def parse_boards(self, response):
        for board_url in response.xpath('//td[@class="alt1Active"]/div/a/@href').extract():
#            print(board_url)
            yield scrapy.Request(board_url, callback=self.parse_page_num, dont_filter=True)        


    def parse_page_num(self, response):
        yield scrapy.Request(response.url, callback=self.parse_topic_list, dont_filter=True)        
        max_page = int(response.xpath('//td[@class="vbmenu_control"]/text()').extract_first().split()[-1])
        for i in range(2,max_page+1):
            url = response.url +"index%d.html"%i
            yield scrapy.Request(url, callback=self.parse_topic_list, dont_filter=True)        

    def parse_topic_list(self, response):
        for post in response.xpath("//a[contains(@id, 'thread_title')]/@href").extract():
#            print(post, '\n')
            url = response.urljoin(post)
            yield scrapy.Request(url, callback=self.parse_topic, dont_filter=True)


    def parse_topic(self, response):
        post = response.xpath('//td[@class="alt1"]/div[2]/text()').extract()
        post = '\n'.join(list(map(lambda x: x.strip(), post)))
        item = HealthboardsItem()
        item['post']=post
        item['url']=response.url
        yield item
#        print(post)
