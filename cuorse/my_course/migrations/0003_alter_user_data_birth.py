# Generated by Django 5.1.4 on 2024-12-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_course', '0002_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='data_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
