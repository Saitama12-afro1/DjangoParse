import asyncio
import re


import aiohttp
from bs4 import BeautifulSoup
from django.core.cache import cache


from .controller import Controller


class Parse:
    __first_url = "http://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes="
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    
    async def get_page(self, url, page):
        key = f'url{page}'
        html = cache.get(key)
        if not html:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), trust_env=True) as session:
                async with session.get(url, headers=self.headers, ssl=False) as response:
                    html = await response.text()
                    await asyncio.sleep(3)
            cache.add(key, value=html)
            
        return html
    
    
    async def get_soup_object(self, url, page = 0):
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
        # print(page, url)
        controller = Controller()
        
        for card in cards:   
            number = card.find("div", {"class" : "registry-entry__header-mid__number"}).find("a").text
            number = re.search(r'[0-9]+', number).group(0)
            try:
                start_price = card.find("div", {"class": "price-block__value"}).text# перевести в float
                start_price = float(re.match(r'[0-9\s]+\,[0-9]+',start_price).group(0).replace("\xa0", "").replace(",", "."))
                result_array.append((number,
                                start_price))
            except AttributeError:
                result_array.append((re.search(r'[0-9]+', number).group(0),
                                0))    
            await controller.create(number, start_price)
        print("apge" + str(page))

           
            
        return result_array

    async def main(self):
        tasks = []
        pagination = await self.get_pagination()
        for i in range(1, 4):
            url = f"http://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={i}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes="
            tasks.append(asyncio.create_task(self.parse(url, i)))
        results = await asyncio.gather(*tasks)
        return results


