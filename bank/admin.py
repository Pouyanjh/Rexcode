from django.contrib import admin

from bank.models import Order, zibal

@admin.register(Order)
class orderadmin(admin.ModelAdmin):
    list_display = ['title', '_id', 'totalprice']
    search_fields = ['_id']

@admin.register(zibal)
class zibaladmin(admin.ModelAdmin):
    list_display = ['Condition', 'lastStatus', 'transId']