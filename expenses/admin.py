from django.contrib import admin

# Register your models here.
from .models import Expense , Category

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount','description','owner','category','date')

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)
