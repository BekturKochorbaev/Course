from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('студент', 'студент'),
        ('преподаватель', 'преподаватель')
        )
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='клиент')
    profile_picture = models.ImageField(upload_to='user_image/', null=True, blank=True)
    bio = models.TextField()


class Category(models.Model):
    category_name = models.CharField(max_length=24, unique=True)


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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField()


class Lesson(models.Model):
    title = models.CharField(max_length=32)
    video_url = models.URLField()
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lesson')


class Assignment(models.Model):
    title = models.CharField(max_length=24)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment_course')
    students = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_students')


class Questions(models.Model):
    questions = models.TextField()


class Exam(models.Model):
    title = models.CharField(max_length=24)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_course')
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='exam_questions')
    passing_score = models.DateField()
    duration = models.TextField()


class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_course')
    issued_at = models.DateField()
    certificate_url = models.URLField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()









