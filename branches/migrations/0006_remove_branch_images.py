# Generated by Django 4.2.15 on 2024-08-27 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0005_alter_branch_images_branchimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='images',
        ),
    ]
