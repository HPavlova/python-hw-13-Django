from django.contrib import admin
from models import CategoryIncome, CategoryExpense, Income, Expense

# Register your models here.
admin.site.register(CategoryIncome)
admin.site.register(CategoryExpense)
admin.site.register(Income)
admin.site.register(Expense)
