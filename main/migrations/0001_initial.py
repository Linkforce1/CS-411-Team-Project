# Generated by Django 2.1.7 on 2019-03-26 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('Email', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('Phone', models.CharField(max_length=14)),
                ('Nickname', models.CharField(max_length=45)),
                ('Gender', models.CharField(max_length=7)),
                ('Password', models.CharField(max_length=255)),
            ],
        ),
    ]
