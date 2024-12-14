from django.urls import path
from .views import UserAnswerListCreateView, ExamListAPIView, ExamDetailAPIView, CourseListAPIView, \
    CourseDetailAPIView, FavoriteListAPIView, FavoriteItemListCreateAPIView, FavoriteItemDeleteUpdateDestroyAPIView, \
    CourseCreateAPIView, CartListAPIView, CartItemListCreateAPIView, CartItemDeleteUpdateDestroyAPIView, \
    CertificateCreateListAPIView, CertificateDeleteUpdateDestroyAPIView, AssignmentCreateListAPIView, \
    AssignmentDeleteUpdateDestroyAPIView

urlpatterns = [
    path('user-answers/', UserAnswerListCreateView.as_view(), name='user-answer-list-create'),

    path('exam/', ExamListAPIView.as_view(), name='exam-list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail'),

    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course_create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),

    path('favorite/', FavoriteListAPIView.as_view(), name='favorite_list'),

    path('favorite_item/', FavoriteItemListCreateAPIView.as_view(), name='favorite_item_list'),
    path('favorite_item/<int:pk>/', FavoriteItemDeleteUpdateDestroyAPIView.as_view(), name='favorite_item_detail'),

    path('cart/', CartListAPIView.as_view(), name='cart_list'),

    path('cart_items/', CartItemListCreateAPIView.as_view(), name='car-item_list'),
    path('cart_items/<int:pk>/', CartItemDeleteUpdateDestroyAPIView.as_view(), name='cart_items'),

    path('certificate_list/', CertificateCreateListAPIView.as_view(), name='certificate_list'),
    path('certificate_list/<int:pk>/', CertificateDeleteUpdateDestroyAPIView.as_view(), name='certificate_delete_update'),

    path('assignment_list/', AssignmentCreateListAPIView.as_view(), name='certificate_list'),
    path('assignment_list/<int:pk>/', AssignmentDeleteUpdateDestroyAPIView.as_view(), name='certificate_delete_update'),

]

