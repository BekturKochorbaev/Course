from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, UserAnswerListCreateView, ExamListAPIView, ExamDetailAPIView, CourseListAPIView, \
    CourseDetailAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты из роутера
    path('user-answers/', UserAnswerListCreateView.as_view(), name='user-answer-list-create'),
    path('exam/', ExamListAPIView.as_view(), name='exam-list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail'),
    path('course/', CourseListAPIView.as_view(), name='exam-detail'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='exam-detail'),


]
