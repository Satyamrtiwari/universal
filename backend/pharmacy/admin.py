from django.contrib import admin
from .models import Pharmacy, Medicine, Stock

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_village', 'pincode', 'phone_number')
    search_fields = ('name', 'area_village')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pharmacy', 'quantity', 'is_available', 'last_updated')
    list_filter = ('is_available', 'pharmacy')
    search_fields = ('medicine__name', 'pharmacy__name')
