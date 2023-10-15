from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.UserList, name='user'),
    path('create_user/',views.Create_User, name='create_user'),
    path('update-user-info/<int:user_id>/', views.update_user_info, name='update_user_info'),
    path('view-user/<int:user_id>', views.view_user, name='view_user'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authenticate/reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="authenticate/reset_password_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/password_reset_complete.html"),
         name="password_reset_complete"),

]