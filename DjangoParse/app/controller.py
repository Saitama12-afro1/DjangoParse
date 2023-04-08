from asgiref.sync import sync_to_async

from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Prefetch

from .models import Detail, Purchase

class Controller:
    @sync_to_async
    def create(self, number, start_price):
        try:
            with transaction.atomic():
                purchase_obj = Purchase.objects.create(purchase_number = number, start_price =start_price)
                Detail.objects.create(purchase = purchase_obj)
        except IntegrityError:
            with transaction.atomic():
                purchase_obj = Purchase.objects.get(purchase_number = number)
                if purchase_obj.start_price != start_price:
                    purchase_obj.start_price = start_price
                    Detail.objects.get_or_create(purchase_id = number)
    
    @staticmethod
    def get_with_one_query():
        return Detail.objects.prefetch_related(
            Prefetch('purchase', queryset=Purchase.objects.only('purchase_number'))
        ).only('calculation', 'purchase_id__purchase_number')