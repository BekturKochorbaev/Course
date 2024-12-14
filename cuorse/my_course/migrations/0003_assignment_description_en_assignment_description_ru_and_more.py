# Generated by Django 5.1.4 on 2024-12-14 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_course', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='title_en',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='title_ru',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_en',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_ru',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='title_en',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='title_ru',
            field=models.CharField(max_length=32, null=True),
        ),
    ]