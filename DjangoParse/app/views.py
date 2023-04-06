import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views import View


from .pasre import Parse

class MyView(View):

    def get(self, request):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        a = loop.run_until_complete(Parse().main())
        
        return HttpResponse(a)

