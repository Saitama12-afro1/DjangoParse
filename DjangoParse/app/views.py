import asyncio


from django.views import View
from django.shortcuts import render


from .pasre import Parse
from .controller import Controller


class MyView(View):
    
    def get(self, request):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        loop.run_until_complete(Parse().main())
        # a = asyncio.run(Parse().main())
        data = Controller.get_with_one_query()
       
        return render(request, "app/index.html",context={'data': data})