from django.urls import path
from .views import IndexView, CreateLpView, UpdateLpView, DeleteLpView, signupuser, loginuser, logoutuser

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', CreateLpView.as_view(), name='add_lp'),
    path('<int:pk>/update/', UpdateLpView.as_view(), name='upd_lp'),
    path('<int:pk>/delete/', DeleteLpView.as_view(), name='del_lp'),

    path('signup/', signupuser, name='signupuser'),
    path('login/', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
]
