# Generated by Django 4.0.6 on 2022-07-19 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortener',
            name='key',
        ),
    ]
