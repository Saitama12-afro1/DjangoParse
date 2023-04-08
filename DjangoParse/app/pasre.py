import asyncio
import re


import aiohttp
from bs4 import BeautifulSoup
from django.core.cache import cache


from .controller import Controller


class Parse:
    __first_url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    
    async def get_page(self, url, page):
        conn = aiohttp.TCPConnector(limit_per_host=1)
        params = [("pageNumber", str(page)),]
        key = f'url{page}'
        html = cache.get(key)
        if not html:
            async with aiohttp.ClientSession(connector=conn,timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.get(url, headers=self.__headers, ssl=True, params = params) as response:
                    html = await response.text()

            cache.add(key, value=html)
            
        return html
    
    
    async def get_soup_object(self, url, page = 1):
        html = await self.get_page(url, page)
        return  BeautifulSoup(html, 'lxml')
    
    
    async def get_pagination(self):
        url = self.__first_url
        soup = await self.get_soup_object(url)
        pagination = soup.find("div", {"class": "paginator-block"}).find("div", {"class": "paginator align-self-center m-0"}).find_all("li")[-1].text
        return int(pagination)
        

    async def parse(self, url, page):
       
        soup =  await self.get_soup_object(url, page)
        
        cards = soup.find_all("div", {"class": "row no-gutters registry-entry__form mr-0"})
        result_array = []
        controller = Controller()
        
        for card in cards:   
            number = card.find("div", {"class" : "registry-entry__header-mid__number"}).find("a").text
            number = re.search(r'[0-9]+', number).group(0)
            try:
                start_price = card.find("div", {"class": "price-block__value"}).text# перевести в float
                start_price = float(re.match(r'[0-9\s]+\,[0-9]+',start_price).group(0).replace("\xa0", "").replace(",", "."))
                result_array.append((number,start_price))
            except AttributeError:
                start_price = 0
                result_array.append((re.search(r'[0-9]+', number).group(0),0))    
            await controller.create(number, start_price)           
        return result_array

    async def main(self):
        tasks = []
        pagination = await self.get_pagination()
        for i in range(1, pagination):
            url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
            tasks.append(asyncio.create_task(self.parse(url, i)))
        results = await asyncio.gather(*tasks)
        return results


