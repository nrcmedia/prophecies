# Generated by Django 3.2.6 on 2021-08-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrecord',
            name='priority',
            field=models.PositiveIntegerField(default=1, verbose_name='Priority'),
        ),
    ]