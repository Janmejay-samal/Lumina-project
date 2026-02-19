from django.contrib import admin
from .models import Student, register
from .models import Product
# Register your models here.
admin.site.register(Student)
admin.site.register(register)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_new', 'is_limited', 'created_at')
    list_filter = ('category', 'is_new', 'is_limited')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_new', 'is_limited')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'price', 'description', 'category', 'image')
        }),
        ('Badges', {
            'fields': ('is_new', 'is_limited'),
            'classes': ('wide',),
        }),
        ('Specifications', {
            'fields': ('spec_1', 'spec_2', 'spec_3'),
        }),
    )