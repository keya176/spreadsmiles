# Generated by Django 3.1 on 2020-08-17 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_moneydonatorinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneydonatorinfo',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
