from rest_framework import viewsets, generics
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


from rest_framework import viewsets, status, generics
from .models import Question, UserAnswer, Choice, Exam, Course, User
from .serializers import (QuestionSerializer, UserAnswerSerializer, ExamListSerializers,
                          ExamDetailSerializers, CourseListSerializers, CourseDetailSerializers)
from rest_framework.response import Response


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer





class UserAnswerListCreateView(generics.ListCreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        user_id = request.data.get('user')  # user_id приходит из запроса
        question_id = request.data.get('question')
        choice_id = request.data.get('choice')

        try:
            # Получаем объект пользователя (используем кастомную модель)
            user = User.objects.get(id=user_id)

            if UserAnswer.objects.filter(user=user, question_id=question_id).exists():
                return Response({"error": "Вы уже ответили на этот вопрос."}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем, существует ли выбранный вариант ответа
            choice = Choice.objects.get(id=choice_id)
            is_correct = choice.is_correct  # Проверяем, правильный ли ответ

            # Создаем или обновляем ответ студента
            user_answer, created = UserAnswer.objects.update_or_create(
                user=user, question_id=question_id,
                defaults={'choice': choice, 'is_correct': is_correct}
            )

            # Формируем сообщение
            message = "Правильно" if is_correct else "Неправильно"

            return Response({
                "user": user.username,
                "question": user_answer.question.text,
                "choice": user_answer.choice.text,
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


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializers


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializers



