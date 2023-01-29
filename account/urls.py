
from django.urls import path
from .import views


urlpatterns = [
    path('login/',views.login,name='login' ),
    path('register/',views.register ,name='register' ),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('logout/',views.logout,name='logout'),
    path('forgotPassword/',views.forgotPassword,name='forgotpassword'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name="reset_password_validate"),
    path('resetPassword/',views.resetPassword,name='resetpassword')
 
]
