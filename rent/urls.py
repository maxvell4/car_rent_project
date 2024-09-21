from django.urls import path
from django.contrib.auth import views as auth_views
from rent import views
from rent.views import (IndexView,
                        AboutUsView,
                        ContactUsView,
                        RentCarView,
                        CarPhotoView,
                        SuccessView,
                        RegisterView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutUsView.as_view(), name='about_us'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('rent/<int:car_id>/', RentCarView.as_view(), name='rent_car'),
    path('car_photo/<int:car_id>/', CarPhotoView.as_view(), name='car_detail'),
    path('success/', SuccessView.as_view(), name='success'),


    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]

app_name = "rent"
