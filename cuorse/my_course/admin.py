from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)


class LessonVideoInline(admin.TabularInline):
    model = LessonVideo
    extra = 1


class LessonFileInline(admin.TabularInline):
    model = LessonFile
    extra = 1


class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonVideoInline, LessonFileInline]


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Exam)
admin.site.register(Certificate)
admin.site.register(Review)
