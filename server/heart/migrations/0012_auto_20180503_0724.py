# Generated by Django 2.0.3 on 2018-05-03 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0011_auto_20180503_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='status',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]