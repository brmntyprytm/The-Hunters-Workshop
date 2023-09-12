# Generated by Django 4.2.5 on 2023-09-12 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_product_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weapons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('attack_rating', models.IntegerField()),
                ('scaling', models.IntegerField()),
                ('requirements', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
