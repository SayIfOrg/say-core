# Generated by Django 4.2.9 on 2024-03-27 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WPPostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post_oid', models.IntegerField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wpsite_set', to='blogging.wpsitemodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
