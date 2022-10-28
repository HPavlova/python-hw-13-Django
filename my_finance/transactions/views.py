from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now
import datetime
from .models import Income, Expense, CategoryIncome, CategoryExpense


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'transactions/transactions.html')
    return render(request, 'base.html')


@login_required(login_url='/auth/login')
def transactions(request):
    user = request.user
    category_income = CategoryIncome.objects.filter(user_id=user).all()
    category_expense = CategoryExpense.objects.filter(user_id=user).all()
    context = {
        'category_income': category_income,
        'category_expense': category_expense,
    }
    return render(request, 'transactions/transactions.html', context)


@login_required(login_url='/auth/login')
def report(request):
    user = request.user
    incomes = Income.objects.filter(user_id=user).order_by('-created_at')
    expenses = Expense.objects.filter(user_id=user).order_by('-created_at')
    incomes_total = sum([i.amount for i in incomes])
    expense_total = sum([e.amount for e in expenses])
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'incomes_total': incomes_total,
        'expense_total': expense_total,
    }
    return render(request, 'transactions/report.html', context)


@login_required(login_url='/auth/login')
def create_income_category(request):
    user = request.user.id
    if request.method == 'POST':
        category_income = request.POST['category_income']
        if category_income == '':
            messages.add_message(request, messages.ERROR, 'Enter category name')
            return render(request, 'transactions/category.html')
        new_category_income = CategoryIncome(category=category_income)
        # new_category_income.user_id = request.user.id
        new_category_income.user_id = User.objects.get(id=user)
        new_category_income.save()
        messages.success(request, 'Income Category added!')
        return render(request, 'transactions/category.html')
    return render(request, 'transactions/category.html')


@login_required(login_url='/auth/login')
def create_expense_category(request):
    user = request.user.id
    if request.method == 'POST':
        category_expense = request.POST['category']
        if category_expense == '':
            messages.add_message(request, messages.ERROR, 'Category is required')
            return render(request, 'transactions/category.html')
        new_category_expense = CategoryExpense(category=category_expense)
        # new_category_expense.user_id = request.user.id
        new_category_expense.user_id = User.objects.get(id=user)
        new_category_expense.save()
        messages.success(request, 'Expense Category added!')
        return render(request, 'transactions/category.html')
    return render(request, 'transactions/category.html')


@login_required(login_url='/auth/login')
def create_income_transaction(request):
    user = request.user
    category_income = CategoryIncome.objects.filter(user_id=user).all()
    if request.method == 'POST':
        amount = request.POST['amount']
        created_at = request.POST['created_at']
        desc = request.POST['desc']
        category_income = request.POST['category']
        if not amount:
            messages.add_message(request, messages.ERROR, 'Amount is required')
            return render(request, 'transactions/transactions.html')
        if created_at == '':
            created_at = now
        new_income = Income(amount=amount, created_at=created_at, desc=desc, category=category_income)
        new_income.user_id = request.user.id
        new_income.save()
        messages.success(request, 'Transaction added!')
        return
    context = {
        'category_income': category_income
    }
    return render(request, 'transactions/transactions.html', context)


@login_required(login_url='/auth/login')
def create_expense_transaction(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        created_at = request.POST['created_at']
        desc = request.POST['desc']
        category = request.POST['category']
        if not amount:
            messages.add_message(request, messages.ERROR, 'Amount is required')
            return render(request, 'transactions/transactions.html')
        if created_at == '':
            created_at = now
        new_expense = Expense(amount=amount, created_at=created_at, desc=desc, category=category)
        new_expense.user_id = request.user.id
        new_expense.save()
        messages.success(request, 'Transaction added!')
        return
    return render(request, 'transactions/transactions.html')


@login_required(login_url='/auth/login')
def delete_income_transaction(request, income_id):
    income = get_object_or_404(Income, pk=income_id, user=request.user)
    income.delete()
    return redirect((reverse('transactions/report.html')))


@login_required(login_url='/auth/login')
def delete_expense_transaction(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, user=request.user)
    expense.delete()
    return redirect((reverse('transactions/report.html')))


@login_required(login_url='/auth/login')
def filter_transaction(request):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        if from_date == '':
            from_date = now() - datetime.timedelta(days=360)
        if to_date == '':
            to_date = now
        incomes = Income.objects.filter(created_at__range=[from_date, to_date])
        expenses = Expense.objects.filter(created_at__range=[from_date, to_date])
        incomes_total = sum([i.amount for i in incomes])
        expense_total = sum([e.amount for e in expenses])
        context = {
            'incomes': incomes,
            'expenses': expenses,
            'incomes_total': incomes_total,
            'expense_total': expense_total,
        }
        return render(request, 'transactions/report.html', context)
    return redirect((reverse('transactions/report.html')))
