# Generated by Django 4.2.4 on 2023-08-23 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('can_affect_books', 'Can affect books'), ('set_book_as_returned', 'Set book as returned'))},
        ),
    ]
