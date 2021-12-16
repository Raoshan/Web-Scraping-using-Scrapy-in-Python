import scrapy
class SquareSpider(scrapy.Spider):
    name = 'square'
    allowed_domains = ['midsouthshooterssupply.com']
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1']

    def parse(self, response):
        for product in response.css('div.product'):
            try:
                title = product.css('a.catalog-item-name::text').get()
            except:
                title = ""  

            try:
                f_price = float(product.css('span.price ::text').get().strip('$'))                  
                price = "${:,.2f}".format(f_price)
            except:
                try:
                    price = ""
                except: 
                    price = ""      

            try:
                stock_status = product.css('span.out-of-stock::text').get()
                if stock_status == 'Out of Stock':
                    stock_status = False   
                                  
            except AttributeError:
                try:
                    stock_status = product.css('span.out-of-stock::text').get()
                    if stock_status=='In Stock':
                        stock_status=True 
                except:
                    stock_status = ""    
            try:
                manufacturer = product.css('a.catalog-item-brand::text').get()
            except:
                manufacturer = ""    

            yield{
                'price':price,
                'title':title,
                'stock':stock_status,
                'maftr':manufacturer
            }

        link = response.xpath('//*[@id="MainContent_dpProductsBottom"]/a[4]/@href').extract()  
        length = len(link)
        if length>0:
            next_page = 'https://www.midsouthshooterssupply.com'+''.join(str(x) for x in link)        
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)   
