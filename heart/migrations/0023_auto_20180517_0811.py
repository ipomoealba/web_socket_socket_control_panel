# Generated by Django 2.0.5 on 2018-05-17 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0022_auto_20180517_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
