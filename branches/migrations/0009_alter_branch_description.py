# Generated by Django 4.2.15 on 2024-09-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0008_alter_branch_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
