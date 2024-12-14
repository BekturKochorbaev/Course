from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


@admin.register(Lesson)
class LessonAdmin(TranslationAdmin):
    inlines = [LessonVideoInline, LessonFileInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Course, Assignment)
class AllAdmin(TranslationAdmin):


    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Cart, CartAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Exam)
admin.site.register(Certificate)
admin.site.register(Review)
