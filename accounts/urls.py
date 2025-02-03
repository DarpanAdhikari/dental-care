from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('manage-accounts/',views.manage_accounts,name='manage-accounts'),
    path('edit-user/<int:user_id>/',views.edit_user,name='edit-user'),
    path('delete/<int:user_id>/',views.delete_user,name='delete-user'),
    path('password/<int:user_id>/',views.change_password,name='change-password'),
    path('user/password/<int:user_id>/',views.user_change_password,name='user-change-password'),
    path('login/',views.login,name='login'),
    path('profile/<str:user_id>/',views.user_profile,name='user-profile'),
    path('logout/',views.logout_view, name='logout'),
    # path('<path:resource>/', views.notfound, name='notfound') #if no url mathces then
]
