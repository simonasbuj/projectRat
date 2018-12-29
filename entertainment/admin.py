from django.contrib import admin
from .models import Wish, Transaction

from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"

# Register your models here.
@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'status', 'accumulation')
    search_fields = ['title']
    list_filter = ('created_at', 'status')

    def accumulation(self, obj):
        return str(obj.get_transaction_sum) + "/" + str(obj.price)
    accumulation.short_description = "Sukaupta EUR"

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    #display in list view
    list_display = ('__str__', 'amount', 'custom_name', 'charge_id', 'is_refunded', )
    search_fields = ['=id', '=charge_id'] #search by, '=' searches EXACT value, without it search is LIKE

    #filter options
    list_filter = ('created_at', 'is_refunded',)
    #fields order in admin form view
    fields = ('charge_id', 'amount', 'email', 'created_at', 'is_refunded', 'refunded_at', 'firstname', 'lastname', 'user', 'wish')
    readonly_fields = ['created_at', 'refunded_at', 'amount', 'email', 'charge_id', 'firstname', 'lastname', 'user']

    #Remove delete action from transaction model
    def has_delete_permission(self, request, obj=None):
        return False

    def custom_name(self, obj):
        return obj.get_formated_date
