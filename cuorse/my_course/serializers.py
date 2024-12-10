from rest_framework import serializers
from .models import Question, Choice, UserAnswer, User, Course, Exam, Lesson, LessonVideo, LessonFile, Teacher


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']  # Добавляем флаг правильного ответа для преподавателя


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class QuestionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['user', 'question', 'choice', 'is_correct']
        read_only_fields = ['is_correct']  # Это поле заполняется автоматически

    def create(self, validated_data):
        # Проверяем правильность ответа
        choice = validated_data['choice']
        is_correct = choice.is_correct

        # Создаем объект ответа с результатом
        validated_data['is_correct'] = is_correct
        return super().create(validated_data)


class CourseSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']


class ExamListSerializers(serializers.ModelSerializer):
    course = CourseSimpleSerializers(read_only=True)
    class Meta:
        model = Exam
        fields = ['title', 'course', 'passing_score', 'duration']


class ExamDetailSerializers(serializers.ModelSerializer):
    questions = QuestionSimpleSerializer(read_only=True, many=True)
    class Meta:
        model = Exam
        fields = ['title', 'questions']


class LessonVideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = ['video']


class LessonFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = LessonFile
        fields = ['file']


class LessonSimpleSerializers(serializers.ModelSerializer):
    video = LessonVideoSerializers(read_only=True, many=True)
    file = LessonFileSerializers(read_only=True, many=True)
    teacher = TeacherSerializers(read_only=True)

    class Meta:
        model = Lesson
        fields = ['title', 'video', 'file', 'teacher']


class CourseListSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()
    created_by = TeacherSerializers(read_only=True)
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['course_name', 'created_by', 'price', 'avg_rating', 'count_rating', 'discount_price']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()

    def get_discount_price(self, obj):
        return obj.get_discount_price()


class CourseDetailSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()
    created_by = TeacherSerializers(read_only=True)
    course_lesson = LessonSimpleSerializers(read_only=True, many=True)


    class Meta:
        model = Course
        fields = ['course_name', 'created_by', 'price', 'avg_rating',
                  'count_rating', 'updated_at', 'description', 'course_lesson']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()

