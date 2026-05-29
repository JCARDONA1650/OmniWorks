from django.urls import path
from . import views

urlpatterns = [
    path('modules/', views.UserModulesView.as_view(), name='user_modules'),
    path('admin/users/<int:user_id>/modules/', views.AdminModulePermissionsView.as_view(), name='admin_module_permissions'),
]
