# Generated by Django 2.0.3 on 2018-05-03 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0010_rule_enable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='default',
        ),
        migrations.AddField(
            model_name='command',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='heart.Device'),
        ),
    ]
