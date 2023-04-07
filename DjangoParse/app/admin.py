from django.contrib import admin

from .models import Purchase, Detail

class PurchaseInLine(admin.StackedInline):
    model = Purchase
    extra = 1

class DetailAdmin(admin.ModelAdmin):

    search_fields = ['purchase__purchase_number']


class DetailInLine(admin.StackedInline):
    model = Detail
    extra = 1


class PurcaseAdmin(admin.ModelAdmin):
    inlines = [DetailInLine]
    search_fields = ['purchase_number']


admin.site.register(Detail,DetailAdmin)
admin.site.register(Purchase, PurcaseAdmin)