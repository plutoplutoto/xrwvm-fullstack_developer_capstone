from django.contrib import admin
from .models import CarMake, CarModel

# Inline class to show CarModel in CarMake admin page
class CarModelInline(admin.TabularInline):  # or use StackedInline for vertical layout
    model = CarModel
    extra = 1  # Number of empty forms to display

# Custom admin for CarModel (optional, but useful for filtering/searching)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ('type', 'year')
    search_fields = ('name', 'car_make__name')

# Custom admin for CarMake with inline CarModels
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    inlines = [CarModelInline]

# Register models with admin site
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
