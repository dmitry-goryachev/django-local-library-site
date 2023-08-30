# Generated by Django 4.2.4 on 2023-08-21 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('view_all_borrowed', 'View all borrowed books'))},
        ),
    ]
