# Generated by Django 4.0.6 on 2023-11-01 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
            },
        ),
    ]
