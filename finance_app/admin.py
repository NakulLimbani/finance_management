from django.contrib import admin
from finance_app.models import Expense , Contact, Income, BankTransaction

admin.site.register(Expense),
admin.site.register(Contact),
admin.site.register(Income),
admin.site.register(BankTransaction),