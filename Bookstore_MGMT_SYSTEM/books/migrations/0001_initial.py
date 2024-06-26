# Generated by Django 4.1 on 2024-03-30 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('authors', models.CharField(max_length=255)),
                ('original_language', models.CharField(max_length=50)),
                ('first_published', models.IntegerField()),
                ('sales_millions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('genre', models.CharField(max_length=100)),
                ('shelves', models.CharField(max_length=50)),
                ('number_of_books', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
