# Generated by Django 4.2.15 on 2024-09-05 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0011_alter_branch_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='description',
            field=models.TextField(default='Lorem ipsum dolor sit amet consectetur adipisicing elit. Error, delectus reprehenderit! Ut provident cum voluptatibus? Consectetur, totam sint quod, autem reprehenderit, eligendi vero nobis consequuntur quasi quos fuga cum esse?'),
            preserve_default=False,
        ),
    ]
