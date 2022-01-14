import scrapy

class rentalSpider(scrapy.Spider):
    name = 'apartments'
    start_urls = ['https://www.apartments.com/apartments/indianapolis-in/1-bedrooms-over-200/']
    
    def parse(self, response):
        for places in response.css('li.mortar-wrapper'):
            try:
                yield {
                    'name': places.css('span.js-placardTitle.title::text').get(),
                    'address': places.css('div.property-address.js-url::text').get(),
                    'min_price': places.css('p.property-pricing::text').get().replace('$', '').replace(',', '').replace(' ', '').split('-', 1)[0],
                    'max_price': places.css('p.property-pricing::text').get().replace('$', '').replace(',', '').replace(' ', '').split('-', 1)[1],
                    'link': places.css('a.property-link').attrib['href']
                }
            except:
                yield {
                    'name': places.css('span.js-placardTitle.title::text').get(),
                    'address': places.css('div.property-address.js-url::text').get(),
                    'min_price': places.css('p.property-pricing::text').get().replace('$', '').replace(',', ''),
                    'max_price': places.css('p.property-pricing::text').get().replace('$', '').replace(',', ''),
                    'link': places.css('a.property-link').attrib['href']
                }

        next_page_value = int(response.css('a.active::text').get()) + 1
        next_page_value = str(next_page_value) 
        next_page = "https://www.apartments.com/apartments/indianapolis-in/1-bedrooms-over-200/" + next_page_value 
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


