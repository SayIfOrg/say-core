# Generated by Django 4.2.11 on 2024-03-30 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0004_wpregistermodel_apikey_alter_wpregistermodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='wpregistermodel',
            name='secret_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]