# Generated by Django 2.0.3 on 2018-05-03 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0013_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='default',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
