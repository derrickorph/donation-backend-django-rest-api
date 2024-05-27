from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LoginView, UserView, LogoutView, IdentificationNumberView, UsersListView, \
    UsersBlockedListView, UserDonationView, UserReceivedDonation, UsersListActivityView

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('user/<int:pk>/change-status', UserView.as_view()),
    path('users', UsersListView.as_view()),
    path('users-list', UsersListActivityView.as_view()),
    path('blocked-users', UsersBlockedListView.as_view()),
    path('logout', LogoutView.as_view()),
    path('id_numbers', IdentificationNumberView.as_view()),
    path('id_numbers/<int:pk>', IdentificationNumberView.as_view()),
    path('user/<int:user_id>/donations', UserDonationView.as_view(), name='user_donations'),
    path('donation_received', UserReceivedDonation.as_view(), name='donation_received'),
    path('user/<int:pk>/donate', UserDonationView.as_view(), name='donate'),
]
