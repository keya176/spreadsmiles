# Generated by Django 3.1 on 2020-08-25 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200825_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='BelongingsDonatorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=264)),
                ('email', models.CharField(blank=True, max_length=264)),
                ('contact', models.CharField(blank=True, max_length=264)),
                ('address', models.CharField(blank=True, max_length=264)),
                ('opinion', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(blank=True, max_length=264, upload_to='')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.event')),
            ],
        ),
    ]
