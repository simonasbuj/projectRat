from django.contrib import admin
from .models import Wish, Transaction

# Register your models here.
admin.site.register(Wish)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    #display in list view
    list_display = ('__str__', 'amount', 'custom_name', 'charge_id', 'is_refunded', )
    search_fields = ['=id', '=charge_id'] #search by, '=' searches EXACT value, without it search is LIKE

    #filter options
    list_filter = ('created_at', 'is_refunded',)
    #fields order in admin form view
    fields = ('charge_id', 'amount', 'email', 'created_at', 'is_refunded', 'refunded_at', 'firstname', 'lastname', 'user', 'wish')
    readonly_fields = ['created_at', 'is_refunded', 'refunded_at']

    def custom_name(self, obj):
        return obj.get_formated_date


