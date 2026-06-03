from django.contrib import admin

from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "badge", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "phone_number", "created_at", "total_price")
    search_fields = ("customer_name", "email", "phone_number")
    list_filter = ("created_at",)
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False
