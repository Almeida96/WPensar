# Generated by Django 3.2 on 2021-04-20 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='quantidade',
            field=models.PositiveIntegerField(null=True),
        ),
    ]