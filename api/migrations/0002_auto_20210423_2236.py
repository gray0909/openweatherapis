# Generated by Django 3.1.7 on 2021-04-23 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=10)),
                ('long', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
