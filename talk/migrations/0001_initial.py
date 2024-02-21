# Generated by Django 5.0.1 on 2024-01-21 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
