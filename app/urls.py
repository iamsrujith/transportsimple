from django.urls import path, include
from .import views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('registration/', views.create_user, name='registration'),
    path('email/', include(email_urls)),
    path('login/', views.login_user, name='login'),
    path('', views.dashboard_view, name='home'),
    path('logout/', views.logout_view,name="logout"),
    path('add-question/', views.add_question, name="add_question"),
    path('add-like/<int:question_id>/', views.add_like, name="add_like"),
    path('add-comment/', views.add_comment, name="add_comment"),
    path('add-comment-like/<int:comment_id>/', views.add_comment_like, name="add_comment_like"),
]