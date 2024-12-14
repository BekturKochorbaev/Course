from rest_framework import serializers
from .models import Question, Choice, UserAnswer, User, Course, Exam, Lesson, LessonVideo, LessonFile, Teacher, Review, \
    Student, Favorite, FavoriteItem, Assignment, Certificate, Category, Cart, CartItem


class TeacherSerializers(serializers.ModelSerializer):
    count_teacher_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['first_name', 'profile_picture', 'last_name', 'position', 'bio', 'count_teacher_rating', 'count_review']

    def get_count_teacher_rating(self, obj):
            return obj.get_count_teacher_rating()

    def get_count_review(self, obj):
            return obj.get_count_review()


class TeacherSimpleSerializers(serializers.ModelSerializer):
      class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']


class StudentSimpleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Student
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
        fields = ['student', 'question', 'choice', 'is_correct']
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

    class Meta:
        model = Lesson
        fields = ['title', 'video', 'file',]


class ReviewSerializers(serializers.ModelSerializer):
    student = StudentSimpleSerializers(read_only=True)

    class Meta:
        model = Review
        fields = ['student', 'date', 'rating', 'comment']


class PopularCourseSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_name', 'avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    @staticmethod
    def get_popular_courses():
        # Получаем курсы с рейтингом >= 3
        return Course.objects.filter(
            course_review__rating__gte=3
        ).distinct()

class CourseCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'category', 'LEVEL', 'price', 'discount', 'updated_at', 'language']

class CourseListSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()
    created_by = TeacherSerializers(read_only=True)
    discount_price = serializers.SerializerMethodField()
    popular_courses = serializers.SerializerMethodField()  # Новое поле для популярных курсов

    class Meta:
        model = Course
        fields = ['course_name', 'created_by', 'price', 'avg_rating',
                  'count_rating', 'discount_price', 'popular_courses']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()

    def get_discount_price(self, obj):
        return obj.get_discount_price()

    def get_popular_courses(self, obj):
        # Получаем популярные курсы через PopularCourseSerializer
        popular_courses = PopularCourseSerializer.get_popular_courses()
        serializer = PopularCourseSerializer(popular_courses, many=True)
        return serializer.data


class CourseDetailSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()
    created_by = TeacherSerializers(read_only=True)
    course_lesson = LessonSimpleSerializers(read_only=True, many=True)
    course_review = ReviewSerializers(read_only=True, many=True)


    class Meta:
        model = Course
        fields = ['course_name', 'created_by', 'price', 'avg_rating',
                  'count_rating', 'updated_at', 'description', 'course_lesson', 'course_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()



class FavoriteItemSerializers(serializers.ModelSerializer):
    course = CourseListSerializers(read_only=True)
    favorite_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')


    class Meta:
        model = FavoriteItem
        fields = ['course', 'favorite_id']


class FavoriteSerializers(serializers.ModelSerializer):
    favorite = FavoriteItemSerializers(read_only=True, many=True)
    class Meta:
        model = Favorite
        fields = ['owner', 'favorite']


class CartItemSerializers(serializers.ModelSerializer):
    course = CourseListSerializers(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')

    class Meta:
        model = CartItem
        fields = ['course', 'cart_id']


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'items']


class CertificateCreateListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['student', 'course', 'issued_at', 'certificate_url']


class AssignmentListCreate(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'course', 'students']