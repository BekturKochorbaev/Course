from django.db.models import Avg
from rest_framework import viewsets, status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Question, UserAnswer, Choice, Exam, Course, User, Student, Cart, Certificate, Assignment, \
    FavoriteItem, Favorite, CartItem, Teacher
from .permissions import CheckOwner
from .serializers import (QuestionSerializer, UserAnswerSerializer, ExamListSerializers,
                          ExamDetailSerializers, CourseListSerializers, CourseDetailSerializers, FavoriteSerializers,
                          FavoriteItemSerializers, CourseCreateSerializers, CartItemSerializers, CartSerializers,
                          CertificateCreateListSerializers, AssignmentListCreate, TeacherLoginSerializer,
                          TeacherFormSerializer, StudentLoginSerializer, StudentFormSerializer,
                          StudentProfileSerializers)
from rest_framework.response import Response


class BaseRegisterView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Teacher Register View
class TeacherRegisterView(BaseRegisterView):
    serializer_class = TeacherFormSerializer


# Student Register View
class StudentRegisterView(BaseRegisterView):
    serializer_class = StudentFormSerializer


# Base Custom Login View
class BaseCustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Teacher Login View
class TeacherCustomLoginView(BaseCustomLoginView):
    serializer_class = TeacherLoginSerializer


# Student Login View
class StudentCustomLoginView(BaseCustomLoginView):
    serializer_class = StudentLoginSerializer


# Base Logout View
class BaseLogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Teacher Logout View
class TeacherLogoutView(BaseLogoutView):
    pass


# Student Logout View
class StudentLogoutView(BaseLogoutView):
    pass


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class UserAnswerListCreateView(generics.ListCreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        student_id = request.data.get('student')  # user_id приходит из запроса
        question_id = request.data.get('question')
        choice_id = request.data.get('choice')

        try:
            # Получаем объект пользователя (используем кастомную модель)
            student = Student.objects.get(id=student_id)

            if UserAnswer.objects.filter(student=student, question_id=question_id).exists():
                return Response({"error": "Вы уже ответили на этот вопрос."}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем, существует ли выбранный вариант ответа
            choice = Choice.objects.get(id=choice_id)
            is_correct = choice.is_correct  # Проверяем, правильный ли ответ

            # Создаем или обновляем ответ студента
            student_answer, created = UserAnswer.objects.update_or_create(
                student=student, question_id=question_id,
                defaults={'choice': choice, 'is_correct': is_correct}
            )

            # Формируем сообщение
            message = "Правильно" if is_correct else "Неправильно"

            return Response({
                "user": student.username,
                "question": student_answer.question.text,
                "choice": student_answer.choice.text,
                "message": message
            }, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)
        except Choice.DoesNotExist:
            return Response({"error": "Выбранный вариант ответа не существует."}, status=status.HTTP_400_BAD_REQUEST)


class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializers


class ExamDetailAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializers


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializers
    permission_classes = [CheckOwner]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.annotate(avg_rating=Avg('course_review__rating'))  # Добавляем аннотацию для среднего рейтинга
    serializer_class = CourseListSerializers
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['avg_rating']  # Поля для сортировки
    ordering = ['-avg_rating']  # Сортировка по убыванию популярности (по умолчанию)
    search_fields = ['course_name']


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializers
    permission_classes = [CheckOwner]


class CertificateCreateListAPIView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateCreateListSerializers


class CertificateDeleteUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateCreateListSerializers


class AssignmentCreateListAPIView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentListCreate


class AssignmentDeleteUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateCreateListSerializers


class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSerializers

    def get_queryset(self):
        return Favorite.objects.filter(owner=self.request.user)


class FavoriteItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FavoriteItemSerializers

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__owner=self.request.user)


class FavoriteItemDeleteUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteItemSerializers

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__owner=self.request.user)


class CartListAPIView(generics.ListAPIView):
    serializer_class = CartSerializers

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializers

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDeleteUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializers

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class StudentProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentProfileSerializers


class StudentProfileListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentProfileSerializers

