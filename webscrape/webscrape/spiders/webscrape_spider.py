from scrapy import Spider, Request
from webscrape.items import WebscrapeItem
from datetime import date, timedelta

class webscrapeSpider(Spider):
    name = "webscrape_spider"
    allowed_urls = ['https://www.billboard.com/charts/']
    start_urls= ['https://www.billboard.com/charts/hot-100/']

    @staticmethod
    def saturdays():
            idx = date.today().isoweekday() #.isoweekday(); Mon=1 .... Sun=7        
            if idx == 6: # when today is Saturday
                start_date = date.today()
            elif idx == 7: # when today is Sunday
                start_date = date.today() - timedelta(1)
            else:
                # When today is not(Sun|Sat), then use Saturday date of last week's
                start_date = date.today() - timedelta(idx+1)
                
            while start_date >= date(1958,8,11): #billboard chart has data starting 1958, August 4th
                yield start_date
                start_date = start_date - timedelta(7)

    def parse(self, response):

        saturday_dates = list([i for i in webscrapeSpider.saturdays()])
        result_urls = ['https://www.billboard.com/charts/hot-100/{}'.format(x) for x in saturday_dates]

    # This yields a new Request object that goes to the new url and then direct Scrapy to parse_result_page, 
    # which we haven't defined yet, to parse the response object we got from each of the urls.        
        for url, date in zip(result_urls, saturday_dates):
            yield Request(url=url, callback=self.parse_result_page, meta={'date':date})


    def parse_result_page(self, response):
        # This fucntion parses the search result page.
        # We are looking for url of the detail page.
        date = response.meta['date']
        musics = response.xpath('//*[@class="chart-list-item__first-row chart-list-item__cursor-pointer"]')
        music_stats = response.xpath('//*[@class="chart-list-item__extra-info"]')

        # Relative xpath for all data
        for (music,music_stat) in zip(musics,music_stats):
            # Title, Artist, Rank data extraccting from 'chart-list-item'
            title = music.xpath('.//span[@class="chart-list-item__title-text"]/text()').extract_first().strip()
            artist = music.xpath('.//div[@class="chart-list-item__artist"]/text()').extract_first().strip()
            if artist == "": # catching outlier artist name due to hyperlink format
                artist = music.xpath('.//div[@class="chart-list-item__artist"]/a/text()').extract_first().strip()
            try:
                rank = music.xpath('.//div[@class="chart-list-item__rank "]/text()').extract_first().strip()
            except:
                rank = response.xpath('//*[@class="chart-list-item__rank chart-list-item__rank--long"]/text()').extract_first().strip()
        # extra_music_detail (-1W Rank, Peak Rank, Weeks on Top 100 Chart)
        # for music_stat in music_stats:
            last_week_rank = music_stat.xpath('.//div[@class = "chart-list-item__last-week"]/text()').extract_first()
            peak_rank = music_stat.xpath('.//div[@class = "chart-list-item__weeks-at-one"]/text()').extract_first()
            weeks_on_chart = music_stat.xpath('.//div[@class = "chart-list-item__weeks-on-chart"]/text()').extract_first()
            # print(title,artist, rank,'===',last_week_rank,peak_rank,weeks_on_chart)

            # Initialize a new WikiItem instance for each movie.


            item = WebscrapeItem()
            item['title'] = title
            item['artist'] = artist 
            item['rank'] = rank
            item['date_'] = date
            item['last_week_rank'] = last_week_rank
            item['peak_rank'] = peak_rank
            item['weeks_on_chart'] = weeks_on_chart
            yield item

            # print(title,artist, rank,'===',last_week_rank,peak_rank,weeks_on_chart)

        #     last_week_rank = music_stat.xpath('.//div[@class = "chart-list-item__last-week"]/text()').extract_first()
        #     peak_rank = music_stat.xpath('.//div[@class = "chart-list-item__weeks-at-one"]/text()').extract_first()
        #     weeks_on_chart = music_stat.xpath('.//div[@class = "chart-list-item__weeks-on-chart"]/text()').extract_first()

        
        # print(title,artist, rank, last_week_rank,peak_rank,weeks_on_chart)












            # yield item