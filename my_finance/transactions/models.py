from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

now = timezone.now()


# Create your models here.
class CategoryIncome(models.Model):
    category = models.TextField(max_length=12, null=False)

    def __str__(self):
        return f"Income categories: {self.category}"


class CategoryExpense(models.Model):
    category = models.TextField(max_length=12, null=False)

    def __str__(self):
        return f"Expense categories: {self.category}"


class Income(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    desc = models.TextField(max_length=150, null=False)
    category = models.ForeignKey(CategoryIncome, on_delete=models.PROTECT)

    def __str__(self):
        return f"Owner: {self.user_id}, Income: {self.amount}, {self.created_at}, {self.desc}, {self.category}"


class Expense(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    desc = models.TextField(max_length=150, null=False)
    category = models.ForeignKey(CategoryExpense, on_delete=models.PROTECT)

    def __str__(self):
        return f"Owner: {self.user_id}, Expense: {self.amount}, {self.created_at}, {self.desc}, {self.category}"
