# Generated by Django 4.0.4 on 2022-05-05 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_management', '0003_family_expanse_family_income_alter_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='expanse',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='family',
            name='income',
            field=models.IntegerField(default=0),
        ),
    ]