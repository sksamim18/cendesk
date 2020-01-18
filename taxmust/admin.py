from django.contrib import admin
from taxmust.models import (
    RootCategory, ParentCategory, Service,
    Contact, Order, Document, Note
)


class OrderAdmin(admin.ModelAdmin):
    fields = ('service', 'customer', 'status', 'payment_status')
    search_fields = ('id', 'customer__customer_name')
    list_display = ['id', 'customer', 'service', 'documents']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')
    search_fields = ('order__id', )


admin.site.register(RootCategory)
admin.site.register(ParentCategory)
admin.site.register(Service)
admin.site.register(Contact)
admin.site.register(Order, OrderAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Note)
