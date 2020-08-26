# Generated by Django 3.1 on 2020-08-25 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_belongingsdonatorinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='belongingsdonatorinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='cover',
            field=models.ImageField(blank=True, default='f.jpg', null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='AdminPickup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=264)),
                ('email', models.CharField(blank=True, max_length=264)),
                ('contact', models.CharField(blank=True, max_length=264)),
                ('address', models.CharField(blank=True, max_length=264)),
                ('opinion', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.event')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.organization')),
            ],
        ),
    ]
