from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# app_name = 'blog'

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<str:slug>', views.detail, name='detail'),
    path('contact', views.contact_view, name="contact"),
    path('about', views.about_view, name="about"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('accounts/login/', views.login_view, name='account_login'),
    path('new_post/', views.new_post_view, name= 'new_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name = "delete_post"),
    path('edit_post/<int:post_id>/', views.edit_post, name = "edit_post"),
    path('publish_post/<int:post_id>/', views.publish_post, name='publish_post'),
    path('comment/delete/<int:id>/', views.delete_comment, name='delete_comment'),
    path('profile/', views.profile, name='profile'),
    path('like/<str:slug>/', views.like_post, name='like_post'),
    
    

    # ✅ Password Reset URLs
     path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

#for media handling

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)