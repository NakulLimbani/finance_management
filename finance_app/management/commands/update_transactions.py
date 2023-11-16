from django.core.management.base import BaseCommand
from finance_app.models import Expense, Income
from finance_app.parsers import parse_bank_statement
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update Expense and Income models from BankStatement model'

    def add_arguments(self, parser):
        parser.add_argument('statement_file', type=str, help='CSV file to update transactions')




    def handle(self, *args, **options):
        statement_file_path = options['statement_file']

        parsed_data = parse_bank_statement(statement_file_path)

        if not parsed_data:
            self.stdout.write(self.style.ERROR('Failed to parse the statement file.'))
            return

        user = User.objects.first()  # Replace this with logic to get the appropriate user

        for data in parsed_data:
            if data['transaction_type'] == 'Expense':
                Expense.objects.create(
                    user=user,
                    date=data['date'],
                    category=data['category'],
                    description=data['description'],
                    amount=data['amount'],
                )
            
            elif data['transaction_type'] == 'Income':
                Income.objects.create(
                    date=data['date'],
                    source=data['category'],
                    description=data['description'],
                    amount=data['amount'],
                )

        self.stdout.write(self.style.SUCCESS('Successfully updated Expense and Income models'))
