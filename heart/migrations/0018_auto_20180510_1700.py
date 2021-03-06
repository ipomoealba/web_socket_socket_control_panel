# Generated by Django 2.0.5 on 2018-05-10 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0017_device_port'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='enable',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='rpn',
        ),
        migrations.AddField(
            model_name='rule',
            name='next_step',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_step', to='heart.Command'),
        ),
        migrations.AddField(
            model_name='rule',
            name='pre_step',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_step', to='heart.Command'),
        ),
    ]
