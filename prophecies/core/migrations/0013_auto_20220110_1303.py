# Generated by Django 3.2.9 on 2022-01-10 13:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_actionaggregate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='allow_multiple_checks',
            field=models.BooleanField(default=False, verbose_name='Allow checkers to check several time the same item'),
        ),
        migrations.AlterField(
            model_name='task',
            name='automatic_round_attributions',
            field=models.BooleanField(default=False, verbose_name='Attribute rounds (if not checked, all checkers will participate in all rounds)'),
        ),
        migrations.AlterUniqueTogether(
            name='taskrecordreview',
            unique_together={('task_record_id', 'checker_id', 'round')},
        ),
    ]
