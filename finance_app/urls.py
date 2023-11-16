from django.urls import path
from finance_app import views

#app_name = 'finance_app'

urlpatterns = [
    path("", views.home, name='home'),  # Define a view for the root path
    path("register", views.register, name='register'),
    path("login/", views.login_request, name='login'),
    path("logout", views.logout_request, name= 'logout'),
    path("expense_list", views.expense_list, name='expense_list'),
    path("add_expense", views.add_expense, name='add_expense'),
    path("income_list", views.income_list, name='income_list'),
    path("add_income", views.add_income, name='add_income'),
    path("saving_list",views.saving_list, name='saving_list'),
    path("contact",views.contact,name='contact'),
    path("about",views.about,name='about'),
    path("upload_bank_statement", views.upload_bank_statement, name='upload_bank_statement'),
    path("save_bank_statement", views.save_bank_statement, name='save_bank_statement'),

    
]
        