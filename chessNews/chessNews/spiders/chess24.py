import scrapy
from chessNews.items import ChessnewsItem
from scrapy.http import Request
import w3lib.html


class Chess24Spider(scrapy.Spider):
    name = 'chess24'
    allowed_domains = ['chess24.com']

    def __init__(self):
        self.start_urls = ['http://chess24.com/en/read/news?limit=100']
        self.n_pages = 22
    
    #This mimics our spider clicking next page.
        for i in range(2, self.n_pages + 2):
            self.start_urls.append('https://chess24.com/en/read/news?ContentNews_page={}&language=en&limit=100'.format(str(i)))

    def parse(self, response):
        #Looping over the links on the next news pages
        for href in response.xpath('//h3/a/@href').extract():
            url = href
            self.start_urls.append(url)
            yield scrapy.Request(url, callback=self.parse_news_article) 
    
    def parse_news_article(self, response):
        item = ChessnewsItem()
        
        item['url'] = response.request.url
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['date'] = response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[1]/span[2]/text()').extract()
        
        item['author'] = response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[1]/span[3]/a/text()').extract()
        
        #This item firstly Requests a new page in order to find the country field there!
        url = 'http://www.chess.24.com/' + response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[1]/span[3]/a/@href').extract_first()
        self.start_urls.append(url)
        
        item['comment_count'] = response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[3]/h2/span/text()').extract_first()
        
        item['category'] = response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[1]/span[1]/@class').extract_first()

        yield item 
        
#         , scrapy.Request(url, callback = self.parse_country)
        
#     def parse_country(self, response):
#         item = ChessnewsItem()
#         item['country'] = response.xpath('/html/body/div[1]/div[2]/div/div[6]/div[3]/div[1]/div[1]/div/div/div/div[1]/div[2]/dl/dd[2]/span/text()').extract_first()
        
#         yield item
        
    
        
