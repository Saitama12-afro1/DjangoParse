import asyncio


from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.db.models import Prefetch


from .pasre import Parse
from .models import Purchase, Detail


class MyView(View):
    
    def get(self, request):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        a = loop.run_until_complete(Parse().main())
        # a = asyncio.run(Parse().main())
        data = Detail.objects.prefetch_related(
            Prefetch('purchase', queryset=Purchase.objects.only('purchase_number'))
        ).only('calculation', 'purchase_id__purchase_number')
        
        return render(request, "app/index.html",context={'data': data})

