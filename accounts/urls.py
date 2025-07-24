from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('forgot-password-validate/<uidb64>/<token>', views.forgot_password_validate, name='forgot-password-validate'),
    path('reset-password', views.reset_password, name='reset-password'),
]
