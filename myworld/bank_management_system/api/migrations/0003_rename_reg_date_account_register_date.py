# Generated by Django 4.2.1 on 2023-06-07 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_client_branch_delete_client_account"),
    ]

    operations = [
        migrations.RenameField(
            model_name="account", old_name="reg_date", new_name="register_date",
        ),
    ]