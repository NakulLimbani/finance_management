# Generated by Django 4.2.5 on 2023-11-07 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0010_rename_transaction_type_banktransaction_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('drink', 'Drink'), ('groceries', 'Groceries'), ('health', 'Health'), ('travel', 'Travel'), ('bills', 'Bills'), ('rent', 'Rent'), ('fashion', 'Fashion'), ('entertainment', 'Entertainment'), ('education', 'Education'), ('other', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='income',
            name='source',
            field=models.CharField(choices=[('salary', 'Salary'), ('bank', 'Bank'), ('freelance', 'Freelance Work'), ('business', 'Business Income'), ('investment', 'Investment Returns'), ('rental', 'Rental Income'), ('side_job', 'Side Job'), ('commission', 'Commission'), ('online_sales', 'Online Sales'), ('other', 'Other')], max_length=255),
        ),
    ]
