from datetime import datetime

import scrapy


class CleMetroSpider(scrapy.Spider):
    name = "clevelandmetroparks_dot_com"

    def start_requests(self):
        urls = [
            'https://clevelandmetroparks.com/parks/learn/blogs/fishing-report',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css('div.horizontal-summary-content-area a'):
            yield response.follow(a, self.parse_blog)

        for a in response.css('div.numbered-pagination-snippet li a'):
            yield response.follow(a, self.parse)

    def parse_blog(self, response):
        yield {
            'raw_timestamp': response.css('span.post-date::text').extract_first(),
            'timestamp': datetime.strptime(response.css('span.post-date::text').extract_first(), '%B %d, %Y'),
            'raw': response.css('div.main-copy-snippet').extract(),
        }

        for a in response.css('div.simple-pagination-snippet a'):
            yield response.follow(a, self.parse_blog)


class LakeMetroSpider(scrapy.Spider):
    name = "lakemetroparks_dot_com"

    def start_requests(self):
        urls = [
            'http://www.lakemetroparks.com/fishing-report',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css('div.main-content-area a.blog-post-link'):
            yield response.follow(a, self.parse_blog)

        for a in response.css('div.pagination-area a'):
            yield response.follow(a, self.parse)

    def parse_blog(self, response):
        raw_timestamp = (response.css('ul.detail-metadata-list')
                                 .re(r'Posted\s[A-Za-z]+\s[0-9]{2},\s[0-9]{4}')[0]
                                 .replace('Posted ', ''))

        yield {
            'raw_timestamp': raw_timestamp,
            'timestamp': datetime.strptime(raw_timestamp, '%B %d, %Y'),
            'raw': response.css('div.main-copy-snippet').extract(),
        }

        for a in response.css('div.detail-navigation-area a'):
            yield response.follow(a, self.parse_blog)


class ArcOrgSpider(scrapy.Spider):
    name = "outdoornews_dot_com"

    def start_requests(self):
        urls = [
            'https://web.archive.org/web/20170322194049/http://www.outdoornews.com/ohio/fishing-reports/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css('div.main-content-area a.blog-post-link'):
            yield response.follow(a, self.parse_blog)

        for a in response.css('div.pagination-area a'):
            yield response.follow(a, self.parse)

    def parse_blog(self, response):
        raw_timestamp = (response.css('ul.detail-metadata-list')
                                 .re(r'Posted\s[A-Za-z]+\s[0-9]{2},\s[0-9]{4}')[0]
                                 .replace('Posted ', ''))

        yield {
            'raw_timestamp': raw_timestamp,
            'timestamp': datetime.strptime(raw_timestamp, '%B %d, %Y'),
            'raw': response.css('div.main-copy-snippet').extract(),
        }

        for a in response.css('div.detail-navigation-area a'):
            yield response.follow(a, self.parse_blog)
