# Generated by Django 5.1.4 on 2024-12-11 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_review', to='my_course.course'),
        ),
        migrations.AlterField(
            model_name='review',
            name='teacher',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_rating', to='my_course.teacher'),
        ),
    ]
