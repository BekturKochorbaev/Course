from django.db.models import Avg
from rest_framework import viewsets, status, generics
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Question, UserAnswer, Choice, Exam, Course, User, Student, Cart, Certificate, Assignment, \
    FavoriteItem, Favorite, CartItem
from .serializers import (QuestionSerializer, UserAnswerSerializer, ExamListSerializers,
                          ExamDetailSerializers, CourseListSerializers, CourseDetailSerializers, FavoriteSerializers,
                          FavoriteItemSerializers, CourseCreateSerializers, CartItemSerializers, CartSerializers,
                          CertificateCreateListSerializers, AssignmentListCreate)
from rest_framework.response import Response


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


