# Generated by Django 5.0.2 on 2024-02-22 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=240),
        ),
    ]