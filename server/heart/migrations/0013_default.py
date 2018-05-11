# Generated by Django 2.0.3 on 2018-05-03 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0012_auto_20180503_0724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coommand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heart.Command')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heart.Device')),
            ],
        ),
    ]