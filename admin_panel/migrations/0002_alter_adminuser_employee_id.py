# Generated by Django 3.2 on 2022-05-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='employee_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]