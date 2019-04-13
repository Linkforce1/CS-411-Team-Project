# Generated by Django 2.1.7 on 2019-04-12 03:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('idRoomNumber', models.IntegerField(primary_key=True, serialize=False)),
                ('RoomName', models.CharField(default='my-room', max_length=45)),
                ('Access', models.CharField(max_length=7)),
                ('Host', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Email', models.EmailField(max_length=254)),
                ('Phone', models.CharField(blank=True, max_length=14, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('Nickname', models.CharField(blank=True, max_length=45)),
                ('Gender', models.CharField(blank=True, max_length=6)),
                ('Password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='Room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Rooms'),
        ),
        migrations.AddField(
            model_name='guest',
            name='User',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Users'),
        ),
    ]
