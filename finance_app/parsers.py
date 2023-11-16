"""
import csv
from finance_app.choices import CATEGORY_CHOICES, SOURCE_CHOICES
from io import TextIOWrapper

def parse_bank_statement(statement_file):
    if statement_file.name.endswith('.csv'):
        # Wrap the uploaded file to make it readable by the CSV reader
        statement_file_wrapper = TextIOWrapper(statement_file, encoding='utf-8')
        csv_reader = csv.reader(statement_file_wrapper)
        
        parsed_data = []

        # Skip the header row if it exists
        next(csv_reader, None)

        for row in csv_reader:
            if len(row) >= 5:
                transaction_date = row[0]
                transaction_type = row[1]
                category = row[2]
                description = row[3]
                amount = float(row[4])

                category = category.lower()
                if category in [c[0] for c in CATEGORY_CHOICES]:
                    transaction_type = 'Expense'
                elif category in [s[0] for s in SOURCE_CHOICES]:
                    transaction_type = 'Income'
                else:
                    transaction_type = 'Other'
                
                transaction_type = transaction_type.lower()
                if transaction_type == 'expense':
                    transaction_type = 'Expense'
                elif transaction_type == 'income':
                    transaction_type = 'Income'
                else:
                    transaction_type = 'Other'

                parsed_data.append({
                    'date': transaction_date,
                    'category': category,
                    'description': description,
                    'amount': amount,
                    'transaction_type': transaction_type,
                })

        return parsed_data
    else:
        return None
"""
import csv
from finance_app.choices import CATEGORY_CHOICES, SOURCE_CHOICES
from io import TextIOWrapper

def parse_bank_statement(statement_file):
    if statement_file.name.endswith('.csv'):
        # Wrap the uploaded file to make it readable by the CSV reader
        statement_file_wrapper = TextIOWrapper(statement_file, encoding='utf-8')
        csv_reader = csv.reader(statement_file_wrapper)
        
        parsed_data = []

        # Skip the header row if it exists
        next(csv_reader, None)

        for row in csv_reader:
            if len(row) >= 5:  # Updated to check for the required columns
                transaction_date = row[0]
                transaction_type = row[1]  # Added transaction_type field
                category = row[2]
                description = row[3]
                amount = float(row[4])

                if transaction_type.lower() == 'income':
                    source = category.lower()
                    if source not in [s[0] for s in SOURCE_CHOICES]:
                        source = 'Other'
                    category = 'Income'
                elif transaction_type.lower() == 'expense':
                    if category.lower() not in [c[0] for c in CATEGORY_CHOICES]:
                        category = 'Other'
                else:
                    transaction_type = 'Other'
                    category = 'Other'

                parsed_data.append({
                    'date': transaction_date,
                    'category': category,
                    'description': description,
                    'amount': amount,
                    'source': source,  # Only set if transaction_type is 'Income'
                    'transaction_type': transaction_type,
                })

        return parsed_data
    else:
        return None
