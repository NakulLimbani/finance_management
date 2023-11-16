from django.shortcuts import  render, redirect
from finance_app.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("http://127.0.0.1:8000/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="finance_app/register.html", context={"register_form":form})

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("http://127.0.0.1:8000/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="finance_app/login.html", context={"login_form":form})


from django.shortcuts import  render, redirect
from finance_app.forms import NewUserForm
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("http://127.0.0.1:8000/")


from django.shortcuts import render, HttpResponse
from datetime import datetime
from django.urls import reverse
from flask import request
from finance_app.models import Contact, Expense , Income
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'finance_app/home.html')
    #return HttpResponse("this is homepage")


import matplotlib.pyplot as plt #For Graphs
from io import BytesIO #Temporary Storage
import base64 #For storing 
from django.db.models import Sum,Avg #For Calculations
from datetime import datetime #For date and time info
import pandas as pd #For DataFrame Opts
from django.contrib.auth.decorators import login_required
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@login_required
def expense_list(request):
    # Filter expenses by user
    expenses = Expense.objects.filter(user=request.user)

    # Filter expenses by date range if provided in the GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        expenses = expenses.filter(date__range=[start_date, end_date]).order_by('date')

    # Check if there are expenses in the selected date range
    if not expenses.exists():
        return render(
            request,
            'finance_app/expense_list.html',
            {'expenses': [], 'plot_image': None, 'total_expenses': 0, 'avg_expenses': None, 'no_expenses_message': "No Expenses in the Selected Date Range"},
        )

    # Calculate total expenses
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum']

    # Calculate total savings
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_savings = calculate_total_savings(request.user, start_date, end_date)

    # Calculate total savings
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_income = calculate_total_income(request.user, start_date, end_date)

    # Calculate total expenses per category
    category_totals = (
        expenses.values('category')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    # Convert expenses to a Pandas DataFrame for plotting
    expense_data = pd.DataFrame(list(expenses.values()))

    # Group expenses by category and calculate total spending
    spending_by_category = expense_data.groupby('category')['amount'].sum()

    # Create a bar chart to visualize spending by category
    fig, ax = plt.subplots()
    ax.set_title('Spending by Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Total Amount (Rs.)')
    ax.bar(spending_by_category.index, spending_by_category.values, width=0.5)
    ax.set_xticklabels(spending_by_category.index, rotation=45)
    plt.tight_layout()

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()
    img_buffer.close()
    plt.close(fig)  # Close the Matplotlib figure to release resources
    


    """
    # Data visualization - create a donut chart for expenses by category
    labels = spending_by_category.index
    values = spending_by_category.values

    # Convert values to percentages
    total = sum(values)
    percentages = [v/total*100 for v in values]

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # Plot the donut chart
    wedges, texts = ax.pie(percentages, wedgeprops=dict(width=0.5), startangle=-40)

    # Annotation properties
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    # Add labels with arrows
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(f"{labels[i]}\n{percentages[i]:.1f}%", xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.set_title("Expenses by Category: A donut")

    # Save the donut chart as an image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data_pie = base64.b64encode(img_buffer.read()).decode()
    img_buffer.close()
    plt.close()
    """
    
     # Data visualization - create a pie chart for expenses by category
    labels = spending_by_category.index  # Access the index directly
    values = spending_by_category.values  # Access the values directly
    #colors = ['red', 'green', 'blue']

    plt.figure(figsize=(8,6))
    pie=plt.pie(values, labels=labels,autopct='%1.2f%%', startangle=0,labeldistance=1.1, pctdistance=0.75, radius=1)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    
    #plt.tight_layout()
    # Add a legend
    #plt.legend(labels, loc='best')
    plt.legend(pie[0],labels, bbox_to_anchor=(1,0.4), loc="center right", fontsize=9, 
           bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.15, bottom=0.15, right=0.70)
    # Save the pie chart as an image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data_pie = base64.b64encode(img_buffer.read()).decode()
    img_buffer.close()
    plt.close()

    return render(
        request,
        'finance_app/expense_list.html',
        {
            'expenses': expenses,
            'plot_image': img_data,
            'img_data_pie': img_data_pie,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'category_totals': category_totals,
            'start_date': start_date,
            'end_date': end_date,
        },
    )


from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required  # Import the login_required decorator

@login_required  # Apply the login_required decorator to this view
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Set the user for the expense before saving
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user to the currently logged-in user
            expense.save()
            messages.success(request, 'Expense added!')
            return redirect('expense_list')

            # Redirect or show a success message
    else:
        form = ExpenseForm()

    return render(request, 'finance_app/add_expense.html', {'form': form})
    #return HttpResponse("this is Add Expense page")


# Income List 

from finance_app.forms import IncomeForm  # If you have an IncomeForm
from django.db.models import Sum
import matplotlib.pyplot as plt


from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseRedirect

@login_required
def income_list(request):
    # Retrieve income records for the currently logged-in user
    incomes = Income.objects.filter(user=request.user)

    # Check if a date range filter is applied
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        # Try to convert start_date and end_date to datetime objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            # Filter income records by date range
            incomes = incomes.filter(date__range=[start_date, end_date]).order_by('date')   
   

    
    # Check if there are income records in the selected date range
    if not incomes.exists():
        return render(
            request,
            'finance_app/income_list.html',
            {
                'incomes': [],
                'plot_image': None,
                'pie_image' : None,
                'total_incomes': 0,
                'avg_incomes': None,
                'no_incomes_message': "No Income Records in the Selected Date Range",
            },
        )

    # Calculate total income
    total_incomes = incomes.aggregate(Sum('amount'))['amount__sum']

    # Calculate total expenses
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_expenses = calculate_total_expenses(request.user, start_date, end_date)

    # Calculate total savings
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_savings = calculate_total_savings(request.user, start_date, end_date)
    
    # Calculate total income per sources
    source_totals = (
        incomes.values('source')
        .annotate(total_amount=Sum('amount'))
        .order_by('source')
    )

    # Create a separate variable for income data
    income_data = pd.DataFrame(list(incomes.values()))

    # Group income by source and calculate total income
    income_by_source = income_data.groupby('source')['amount'].sum()

    # Create a bar chart to visualize income by source
    fig, ax = plt.subplots()
    ax.set_title('Income by Sources')
    ax.set_xlabel('Source')
    ax.set_ylabel('Total Amount (Rs.)')
    ax.bar(income_by_source.index, income_by_source.values, width=0.5)
    ax.set_xticklabels(income_by_source.index, rotation=45)
    plt.tight_layout()

    img_buffer1 = BytesIO()
    fig.savefig(img_buffer1, format='png')
    img_buffer1.seek(0)
    img_data1 = base64.b64encode(img_buffer1.read()).decode()
    img_buffer1.close()

    plt.close(fig)  # Close the Matplotlib figure to release resources


    # Data visualization - create a pie chart for expenses by category
    labels = income_by_source.index  # Access the index directly
    values = income_by_source.values  # Access the values directly
    #colors = ['red', 'green', 'blue']  # You can define your own color scheme

    plt.figure(figsize=(8,6))
    pie=plt.pie(values, labels=labels,autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    # Add a legend
    plt.legend(pie[0],labels, bbox_to_anchor=(1,0.4), loc="center right", fontsize=10, 
           bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.15, bottom=0.15, right=0.70)

    # Save the pie chart as an image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data_pie = base64.b64encode(img_buffer.read()).decode()
    img_buffer.close()
    plt.close()

    return render(
        request,
        'finance_app/income_list.html',
        {
            'incomes': incomes,
            'plot_image': img_data1,
            'pie_image' : img_data_pie,
            'total_incomes': total_incomes,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'source_totals': source_totals,
            'start_date': start_date,
            'end_date': end_date,
        },
    )

# Add Income
from .forms import IncomeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income Added!')
            # You can add a success message here if needed
            return redirect('income_list')  # Redirect to the income list page after successfully adding income
    else:
        form = IncomeForm()

    return render(request, 'finance_app/add_income.html', {'form': form})

# Savings List

from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Sum
from .models import Income, Expense
#  For Data Visualisation
import matplotlib.pyplot as plt
import io
import base64
from django.core.exceptions import ObjectDoesNotExist


@login_required
def saving_list(request):
    try:
        # Get the selected start and end months from the request
        start_month = request.GET.get('start_month')
        end_month = request.GET.get('end_month')

        # Check if start_month and end_month are provided
        if start_month and end_month and start_month != end_month:
            try:
                # Convert start_month and end_month to datetime objects
                start_date = datetime.strptime(start_month, "%Y-%m")
                end_date = datetime.strptime(end_month, "%Y-%m")

                # Calculate the start of the previous month
                prev_month_start = (start_date - timedelta(days=start_date.day)).replace(day=1)
            
                # Calculate the end of the previous month
                prev_month_end = end_date - timedelta(days=1)

                # Query income records for the selected period
                incomes = Income.objects.filter(user=request.user, date__gte=start_date, date__lte=prev_month_end).order_by('date')

                # Query expense records for both the selected period and the previous month
                expenses = Expense.objects.filter(user=request.user, date__gte=start_date, date__lte=prev_month_end)

                # Calculate net savings (total income - total expenses)
                total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
                total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
                net_savings = total_income - total_expenses

                
                # Create a list of monthly savings data
                savings_data = []
                current_month = start_date

                while current_month < end_date:
                    month_start = current_month
                    month_end = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                    month_incomes = incomes.filter(date__gte=month_start, date__lte=month_end)
                    month_expenses = expenses.filter(date__gte=month_start, date__lte=month_end)
                    month_total_income = month_incomes.aggregate(total=Sum('amount'))['total'] or 0
                    month_total_expenses = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
                    month_savings = month_total_income - month_total_expenses

                    savings_data.append({
                        'month': current_month.strftime("%B, %Y"),
                        'income': month_total_income,
                        'expense': month_total_expenses,
                        'savings': month_savings,
                    })

                    current_month = (current_month + timedelta(days=32)).replace(day=1)

            except ValueError as e:
                return render(request, 'error_template.html', {'error_message': 'Invalid date format. Date must be in YYYY-MM format.'})
        else:
            # If no date range is provided, show data for all months
            incomes = Income.objects.filter(user=request.user)
            expenses = Expense.objects.filter(user=request.user)
            total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
            total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
            net_savings = total_income - total_expenses
            savings_data = [] 

            # Create a list of all months' savings data
            current_month = min(incomes.earliest('date').date, expenses.earliest('date').date)
            end_date = max(incomes.latest('date').date, expenses.latest('date').date)

            while current_month <= end_date:
                month_start = current_month
                month_end = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                month_incomes = incomes.filter(date__gte=month_start, date__lte=month_end)
                month_expenses = expenses.filter(date__gte=month_start, date__lte=month_end)
                month_total_income = month_incomes.aggregate(total=Sum('amount'))['total'] or 0
                month_total_expenses = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
                month_savings = month_total_income - month_total_expenses

                savings_data.append({
                    'month': current_month.strftime("%B, %Y"),
                    'income': month_total_income,
                    'expense': month_total_expenses,
                    'savings': month_savings,
                })

                current_month = (current_month + timedelta(days=32)).replace(day=1)

        
        
        # Data visualization - create a pie chart for expenses vs savings
        labels = ['Expenses', 'Savings']
        sizes = [total_expenses, net_savings]
        colors = ['red', 'green']

        #plt.figure(figsize=(6, 4))
        """ plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
        """
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        plt.tight_layout()
    
        # Add a legend
        plt.legend(labels, loc='best')

        # Save the pie chart as an image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_data3 = base64.b64encode(img_buffer.read()).decode()
        img_buffer.close()
        plt.close()


        # Data visualization - create a bar chart for savings per month
        months = [entry['month'] for entry in savings_data]
        savings = [entry['savings'] for entry in savings_data]

        #plt.figure(figsize=(10, 6))    
        plt.title('Savings per Month')
        plt.xlabel('Month')
        plt.ylabel('Savings')
        plt.bar(months, savings)
        plt.xticks(rotation=45)
        plt.tight_layout()
        


        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_data_bar = base64.b64encode(img_buffer.read()).decode()
        img_buffer.close()
        plt.close()

        
        bar_chart_img_static = create_savings_bar_chart(request)

        # Create a line chart image
        line_chart_img = create_savings_line_chart(request)

        context = {
            'start_month': start_month,
            'end_month': end_month,
            'incomes': incomes,
            'expenses': expenses,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_savings': net_savings,
            'savings_data': savings_data,
            'chart_image': img_data3,
            'bar_chart_image': img_data_bar,
            'bar_chart_image_static': bar_chart_img_static,
            'line_chart_image': line_chart_img,
        }

        return render(request, 'finance_app/saving_list.html', context)

    except ObjectDoesNotExist:
        # Handle the case when income and expense records do not exist
        return render(
            request,
            'finance_app/saving_list.html',
            {
                'start_month': None,
                'end_month': None,
                'incomes': [],
                'expenses': [],
                'total_income': 0,
                'total_expenses': 0,
                'net_savings': 0,
                'savings_data': [],
                'chart_image': None,
                'bar_chart_image': None,
                'bar_chart_image_static': None,
                'line_chart_image': None,
                'no_incomes_message': "No Income Records in the Selected Date Range",
            },
        )


# Function to create a bar chart for savings per month
import matplotlib.pyplot as plt
import io
import base64

# Function to create a bar chart for "Savings per Month"
def create_savings_bar_chart(request):


    # If no date range is provided, show data for all months
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_savings = total_income - total_expenses
    savings_data1 = [] 

    # Create a list of all months' savings data
    current_month = min(incomes.earliest('date').date, expenses.earliest('date').date)
    end_date = max(incomes.latest('date').date, expenses.latest('date').date)

    while current_month <= end_date:
        month_start = current_month
        month_end = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        month_incomes = incomes.filter(date__gte=month_start, date__lte=month_end)
        month_expenses = expenses.filter(date__gte=month_start, date__lte=month_end)
        month_total_income = month_incomes.aggregate(total=Sum('amount'))['total'] or 0
        month_total_expenses = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
        month_savings = month_total_income - month_total_expenses

        savings_data1.append({
            'month': current_month.strftime("%B, %Y"),
            'income': month_total_income,
            'expense': month_total_expenses,
            'savings': month_savings,
        })

        current_month = (current_month + timedelta(days=32)).replace(day=1)
        
    # Data visualization - create a bar chart for savings per month
    months = [entry['month'] for entry in savings_data1]
    savings = [entry['savings'] for entry in savings_data1]

    #plt.figure(figsize=(10, 6))
    """ 
    plt.bar(months, savings, color='green')
    plt.xlabel('Month')
    plt.ylabel('Savings')
    plt.title('All Months Savings')
    plt.xticks(rotation=45)
    plt.tight_layout()"""

    fig, ax = plt.subplots()
    ax.set_title('All Month Savings ')
    ax.set_xlabel('Month')
    ax.set_ylabel('Savings')
    ax.bar(months, savings, color='green')
    #ax.xticks(rotation=45)
    plt.tight_layout()
    

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data4 = base64.b64encode(img_buffer.read()).decode()
    img_buffer.close()
    plt.close()

    return img_data4

import io
import base64
from datetime import datetime, timedelta
from django.shortcuts import render
from finance_app.models import Expense, Income
from django.db.models import Sum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Function to create Linechart for "Savings vs Expense"
def create_savings_line_chart(request):
    try:
        # If no date range is provided, show data for all months
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)
        total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        net_savings = total_income - total_expenses
        savings_data = []

        # Create a list of all months' savings data
        current_month = min(incomes.earliest('date').date, expenses.earliest('date').date)
        end_date = max(incomes.latest('date').date, expenses.latest('date').date)

        while current_month <= end_date:
            month_start = current_month
            month_end = (current_month.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            month_incomes = incomes.filter(date__gte=month_start, date__lte=month_end)
            month_expenses = expenses.filter(date__gte=month_start, date__lte=month_end)
            month_total_income = month_incomes.aggregate(total=Sum('amount'))['total'] or 0
            month_total_expenses = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
            month_savings = month_total_income - month_total_expenses

            savings_data.append({
                'month': current_month.strftime("%B, %Y"),
                'income': month_total_income,
                'expense': month_total_expenses,
                'savings': month_savings,
            })

            current_month = (current_month + timedelta(days=32)).replace(day=1)

        # Create a line chart
        months = [entry['month'] for entry in savings_data]
        expenses = [entry['expense'] for entry in savings_data]
        savings = [entry['savings'] for entry in savings_data]

        fig, ax = plt.subplots()
        ax.plot(months, expenses, label='Expenses', marker='o', linestyle='-', color='red')
        ax.plot(months, savings, label='Savings', marker='o', linestyle='-', color='green')

        ax.set(xlabel='Month', ylabel='Amount',title='Savings vs Expenses Over Time')
        ax.legend(loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        img_buffer = io.BytesIO()
        canvas.print_png(img_buffer)
        img_data2 = base64.b64encode(img_buffer.getvalue()).decode()
        img_buffer.close()
        plt.close()

        return img_data2

    except Exception as e:
        return None


# Contact Us   

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'finance_app/contact.html')    
    #return HttpResponse("This Is Contact Us Page")


def about(request): 
    #return HttpResponse("This Is About Us Page")
    return render(request,'finance_app/about.html')





from django.db.models import Sum
from .models import Expense

def calculate_total_expenses(user, start_date, end_date):
    # Filter expenses by the user and date range
    expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])

    # Calculate the total expenses
    total_expenses = expenses.aggregate(total=Sum('amount'))

    # Return the total expenses or 0 if no expenses found
    return total_expenses['total'] or 0

# Calculating Total Income 
#from django.db.models import Income,Sum
from finance_app.models import Income


def calculate_total_income(user, start_date, end_date):
    total_income = (
        Income.objects.filter(user=user, date__range=[start_date, end_date])
        .aggregate(total=Sum('amount'))
    )
    return total_income['total'] or 0  # Return 0 if no income found

# Calculating Total Savings
def calculate_total_savings(user, start_date, end_date):
    total_income = calculate_total_income(user, start_date, end_date)
    total_expenses = calculate_total_expenses(user, start_date, end_date)  # You need to implement this function.
    total_savings = total_income - total_expenses
    return total_savings



# Parsing Bank Statement

from django.shortcuts import render, redirect
from finance_app.forms import BankStatementUploadForm
from finance_app.parsers import parse_bank_statement
from finance_app.models import BankTransaction  # Import your BankTransaction model
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from django.http import HttpResponse
from finance_app.models import Income, Expense
from django.contrib import messages


def upload_bank_statement(request):
    if request.method == 'POST':
        form = BankStatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            statement_file = form.cleaned_data['statement_file']

            # Ensure the user is authenticated and has permission to upload
            if request.user.is_authenticated:
                user = request.user
            else:
                messages.error(request, 'Please log in to upload statements.')
                return redirect('login')  # Redirect to login page

            parsed_data = parse_bank_statement(statement_file)
            if parsed_data:
                try:
                    for data in parsed_data:
                        if data['transaction_type'] == 'Expense':
                            Expense.objects.create(
                                user=user,
                                date=data['date'],
                                category=data['category'],
                                description=data['description'],
                                amount=data['amount']
                            )
                        elif data['transaction_type'] == 'Income':
                            Income.objects.create(
                                user=user,
                                date=data['date'],
                                source=data['category'],  # Using source instead of category
                                description=data['description'],
                                amount=data['amount']
                            )
                        else:
                            # Handle 'Other' transactions or any unknown types
                            pass

                    messages.success(request, 'Successfully Uploaded!')
                    return redirect('home')  # Redirect to the home page after successful upload
                except Exception as e:
                    messages.error(request, 'An error occurred while processing the statement.')
            else:
                messages.error(request, 'Invalid Statement File.')
    else:
        form = BankStatementUploadForm()

    return render(request, 'finance_app/upload_bank_statement.html', {'form': form})



def save_bank_statement(request):
    if request.method == 'POST':
        # Add your logic to save the transactions to your database
        # Use the BankTransaction model to save the data
        # For example, you can use a try-except block to handle exceptions
        try:
            transactions = BankTransaction.objects.filter(user=request.user)
            total_amount = 0

            for transaction in transactions:
                total_amount += transaction.amount

            messages.success(request, 'Successfully Saved!')
            return redirect("home")  # Redirect to a success page
        except Exception as e:
            # Handle any exceptions or errors that may occur during the saving process
            messages.error(request,"Error Saving File!")
            return redirect('home')
    else:
        # Handle GET request (possibly an error)
        messages.error(request,"Error Saving File!")
        return redirect('home')




 