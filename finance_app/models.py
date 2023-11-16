from django.db import models
from django.contrib.auth.models import User
from finance_app.choices import CATEGORY_CHOICES , SOURCE_CHOICES


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=400)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    description = models.CharField(max_length=400) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
      
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        #return f'{self.user.username} - {self.date} - {self.description}'
        return self.name

class BankTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, default="Unknown")  # Add this field

    def __str__(self):
        return self.description


