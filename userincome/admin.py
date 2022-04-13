from django.contrib import admin

# Register your models here.
from .models import UserIncome , Source

# Register your models here.
class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('amount','description','owner','source','date')

admin.site.register(UserIncome,UserIncomeAdmin)
admin.site.register(Source)

