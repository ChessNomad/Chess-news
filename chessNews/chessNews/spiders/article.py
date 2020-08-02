import scrapy
from chessNews.items import ChessnewsItem
from scrapy.http import Request
import w3lib.html

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['chess.com']
    
    
    def __init__(self):
        self.start_urls = ['http://www.chess.com/news']
        self.n_pages = 399
    
    #This mimics our spider clicking next page.
        for i in range(2, self.n_pages + 2):
            self.start_urls.append('http://www.chess.com/news?page={}'.format(str(i)))

    def parse(self, response):
        #Looping over the links on the next news pages
        for href in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post-preview-title", " " ))]/@href').extract():
            url = href
            self.start_urls.append(url)
            yield scrapy.Request(url, callback=self.parse_news_article) 
    
    def parse_news_article(self, response):
        item = ChessnewsItem()
        
        item['url'] = response.request.url
        item['title'] = w3lib.html.remove_tags(response.xpath('//h1').extract_first())
        item['date'] = response.xpath('//*[@id="view-news-single"]/div[2]/div/article/div[2]/div/div/div[2]/time/@datetime').extract_first()
        item['author'] = response.xpath('//*[@id="view-news-single"]/div[2]/div/article/div[2]/div/div/div[1]/a/@v-user-popover').extract()[0]
        
        item['country'] = response.xpath('//*[@id="view-news-single"]/div[2]/div/article/div[2]/div/div/div[1]/div/@v-tooltip').extract()[0]
        
        item['comment_count'] = w3lib.html.remove_tags(response.xpath('//*[@id="view-news-single"]/div[2]/div/article/div[2]/div/div/div[2]/span[2]').extract_first())
        
        item['category'] = response.xpath('//*[@id="view-news-single"]/div[2]/div/article/div[2]/div/div/div[2]/a/@title').extract()[0]
        item['img_title'] = w3lib.html.remove_tags(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post-view-caption", " " ))]').extract_first())

        yield item
