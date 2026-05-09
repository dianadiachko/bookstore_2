from .models import Order, OrderItem
from django.contrib import admin
from .models import Book, Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ('title', 'author', 'price', 'year', 'stock', 'is_available')
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BookInline]
    search_fields = ('name', 'description')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'is_available', 'year', 'created_at')
    list_filter = ('category', 'is_available', 'year')
    search_fields = ('title', 'author', 'genre', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'created_at', 'paid')
    inlines = [OrderItemInline]