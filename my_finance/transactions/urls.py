from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions, name='index'),
    path('report', views.report, name='report'),
    path('category_income', views.create_income_category, name='category_income'),
    path('category_expense', views.create_expense_category, name='category_expense'),
    path('category_directory', views.category_directory, name='category_directory'),
    path('delete_category_income/<int:category_id>', views.delete_category_income, name='delete_category_income'),
    path('delete_category_expense/<int:category_id>', views.delete_category_expense, name='delete_category_expense'),
    path('income', views.create_income_transaction, name='income'),
    path('expense', views.create_expense_transaction, name='expense'),
    path('delete_income/<int:income_id>', views.delete_income_transaction, name='delete_income'),
    path('delete_expense/<int:expense_id>', views.delete_expense_transaction, name='delete_expense'),
    path('filter', views.filter_transaction, name='filter'),
]
