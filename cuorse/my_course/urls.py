from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='users')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'course', CourseViewSet, basename='courses')
router.register(r'lesson', LessonViewSet, basename='lessons')
router.register(r'assignment', AssignmentViewSet , basename='assignments')
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'exam', ExamViewSet, basename='exams')
router.register(r'certificate', CertificateViewSet, basename='certificate')
router.register(r'review', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    ]

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

