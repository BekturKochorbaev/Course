from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('OTHER', 'OTHER'),
    )

class User(AbstractUser):
    pass


class Teacher(User):
    address = models.CharField(max_length=54)
    gender = models.CharField(max_length=10, choices=GENDER)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    data_birth = models.DateField()
    education = models.CharField(max_length=100)
    work_experience = models.PositiveSmallIntegerField()
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(max_length=15, choices=[('teacher', 'teacher')], default='teacher')
    profile_picture = models.ImageField(upload_to='teacher_profile_picture', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Student(User):
    gender = models.CharField(max_length=10, choices=GENDER)
    age = models.PositiveIntegerField()
    phone_number = PhoneNumberField(null=True, blank=True)
    data_birth = models.DateField()
    role = models.CharField(max_length=15, choices=[('student', 'student')], default='student')
    profile_picture = models.ImageField(upload_to='student_profile_picture', null=True, blank=True)
    bio = models.TextField()


class Category(models.Model):
    category_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.category_name


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
    discount = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField()
    language = models.CharField(max_length=24)

    def __str__(self):
        return self.course_name


    def get_discount_price(self):
         if self.discount is None:
            return 0
         discount = (self.discount * self.price) / 100
         return self.price - discount


    def get_avg_rating(self):
        ratings = self.course_review.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0

    def get_count_rating(self):
        ratings = self.course_review.all()
        if ratings.exists():
            return ratings.count()
        return 0


class Lesson(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lesson')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return self.title


class LessonVideo(models.Model):
    video = models.URLField(null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='video')

    def __str__(self):
        return f"{self.lesson}-videos"


class LessonFile(models.Model):
    file = models.FileField(upload_to='lesson_files/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='file')

    def __str__(self):
        return f"{self.lesson}-files"


class Assignment(models.Model):
    title = models.CharField(max_length=24)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment_course')
    students = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_students')

    def __str__(self):
        return self.title


class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_course')
    issued_at = models.DateField()
    certificate_url = models.URLField()

    def __str__(self):
        return f'{self.student} - {self.course}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user}-{self.rating}'


class Exam(models.Model):
    title = models.CharField(max_length=24)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_course')
    passing_score = models.PositiveIntegerField(default=50)
    duration = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=255)  # Текст вопроса
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Choice(models.Model):  # Ответ
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)  # Связь с вопросом
    text = models.CharField(max_length=255)  # Текст варианта ответа
    is_correct = models.BooleanField(default=False)  # Флаг правильного ответа

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Выбранный пользователем ответ
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # Результат проверки (правильно/неправильно)

    def __str__(self):
        return f"{self.user} - {self.question.text}: {self.choice.text} ({'Correct' if self.is_correct else 'Wrong'})"


