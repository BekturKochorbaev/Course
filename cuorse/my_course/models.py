from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('клиент', 'клиент'),
        ('преподаватель', 'преподаватель')
        )
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='клиент')
    profile_picture = models.ImageField(upload_to='user_image/', null=True, blank=True)
    bio = models.TextField()


class Category(models.Model):
    category_name = models.CharField(max_length=24, unique=True)


class Lesson(models.Model):
    title = models.CharField(max_length=32)
    video_url = models.URLField()
    content = models.TextField()
    course = models.URLField()


class Course(models.Model):
    course_name = models.CharField(max_length=24)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    LEVEL_CHOICES = (
        ('начальный', 'начальный'),
        ('средний', 'средний'),
        ('продвинутый', 'продвинутый')
        )
    LEVEL = models.CharField(max_length=16, choices=LEVEL_CHOICES, default='начальный')
    price = models.PositiveIntegerField()
    created_by = models.URLField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_course')


class Assignment(models.Model):
    title = models.CharField(max_length=24)
    description = models.TextField()
    due_date = models.DateField()
    course = models.URLField()
    students = models.URLField()


class Questions(models.Model):

    questions = models.TextField()


class Exam(models.Model):
    title = models.CharField(max_length=24)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE)
    passing_score = models.PositiveSmallIntegerField(default=50)
    duration = models.TextField()


class Certificate(models.Model):
    student = models.URLField()
    course = models.URLField()
    issued_at = models.DateField()
    certificate_url = models.URLField()


class Review(models.Model):
    user = models.URLField()
    course = models.URLField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

