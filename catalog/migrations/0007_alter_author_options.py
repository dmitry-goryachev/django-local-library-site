# Generated by Django 4.2.4 on 2023-08-16 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_author_date_of_birth'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['id', 'last_name', 'first_name']},
        ),
    ]