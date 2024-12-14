from .models import Course, Lesson, Assignment
from modeltranslation.translator import TranslationOptions, register


@register(Course)
class StoreTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Lesson)
class StoreTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Assignment)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')