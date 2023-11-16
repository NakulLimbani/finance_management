# Expense Form
from django import forms
from finance_app.models import Expense
from finance_app.choices import CATEGORY_CHOICES

class ExpenseForm(forms.ModelForm):
    # Override the category field to use a ChoiceField
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['date', 'category', 'description', 'amount']


# Income Form
from django import forms
from finance_app.models import Income  # import the Income model
from finance_app.choices import SOURCE_CHOICES

class IncomeForm(forms.ModelForm):
    # Override the category field to use a ChoiceField
    source = forms.ChoiceField(choices=SOURCE_CHOICES, widget=forms.Select())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Income
        fields = ['date', 'source', 'description', 'amount']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create User Form

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
      
# Create Bank Statement Upload Form
from django import forms

class BankStatementUploadForm(forms.Form):
    statement_file = forms.FileField(label='Select a bank statement file')
