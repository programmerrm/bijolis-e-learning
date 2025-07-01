from django.urls import path
from api.accounts.views.login import LoginView

urlpatterns = [
    path(
        'user/login/',
        LoginView.as_view(),
        name='login',
    ),
]
