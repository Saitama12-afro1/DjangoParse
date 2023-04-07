import asyncio
from asgiref.sync import sync_to_async

from django.db import transaction
from django.db.utils import IntegrityError

from .models import Detail, Purchase

class Controller:
    @sync_to_async
    def create(self, number, start_price):
        try:
            with transaction.atomic():
                purchase_obj = Purchase.objects.create(purchase_number = number, start_price =start_price)
                Detail.objects.create(purchase = purchase_obj)
        except IntegrityError as e:
            with transaction.atomic():
                purchase_obj = Purchase.objects.get(purchase_number = number)
                if purchase_obj.start_price != start_price:
                    purchase_obj.start_price = start_price
                    Detail.objects.get_or_create(purchase_id = number)
                
        return 0 
    