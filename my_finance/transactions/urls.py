from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions, name='index'),
    path('report/', views.report, name='report'),
    path('income/', views.create_income_transaction, name='income'),
    path('expense/', views.create_expense_transaction, name='expense'),
    path('delete_income/<int:income_id>/', views.delete_income_transaction, name='delete_income'),
    path('delete_expense/<int:expense_id>/', views.delete_expense_transaction, name='delete_expense'),
    path('filter/', views.filter_transaction, name='filter'),
]
