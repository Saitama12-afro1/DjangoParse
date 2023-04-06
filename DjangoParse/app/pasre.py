import asyncio
import re


import aiohttp
from bs4 import BeautifulSoup


class Parse:

    
    async def get_page(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.get(url, headers= headers) as response:
                print(response.status)
                return await response.text()
    
    
    async def get_pagination(self):
        pass

    async def parse(self, url):
        html = await self.get_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all("div", {"class": "row no-gutters registry-entry__form mr-0"})
        result_array = []
        for card in cards:
            number = card.find("div", {"class" : "registry-entry__header-mid__number"}).find("a").text
            print(re.search(r'[0-9]+', number).group(0))
            # print(number.replace(" ", ""))
            start_price = card.find("div", {"class": "price-block__value"}).text# перевести в float
            # a = len((re.match(r'[0-9\s]+\,[0-9]+',start_price).group(0).replace("\xa0", "").replace(",", ".")))

            result_array.append((re.search(r'[0-9]+', number).group(0),
                                float(re.match(r'[0-9\s]+\,[0-9]+',start_price).group(0).replace("\xa0", "").replace(",", "."))))
        
        return result_array

    async def main(self):
        tasks = []
        for i in range(1, 50):
            url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={i}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes="
            tasks.append(asyncio.create_task(self.parse(url)))
        results = await asyncio.gather(*tasks)
        return results
