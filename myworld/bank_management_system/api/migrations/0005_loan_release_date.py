# Generated by Django 4.2.1 on 2023-06-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_rename_paid_loan_balance_remove_loan_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="release_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]