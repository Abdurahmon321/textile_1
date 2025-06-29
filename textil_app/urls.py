from django.urls import path
from . import views
from .views import (
    MaterialListCreateAPIView,
    MaterialRetrieveUpdateDestroyAPIView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/user/create/', views.user_create, name='user_create'),
    path('admin-panel/user/<int:pk>/update/', views.user_update, name='user_update'),
    path('admin-panel/user/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Ranglar (Color) CRUD
    path('admin-panel/colors/', views.color_list, name='color_list'),
    path('admin-panel/colors/create/', views.color_create, name='color_create'),
    path('admin-panel/colors/<int:pk>/update/', views.color_update, name='color_update'),
    path('admin-panel/colors/<int:pk>/delete/', views.color_delete, name='color_delete'),

    # To'quv mashinalarini boshqarish
    path('admin-panel/tikuv-mashinalar/', views.tikuv_mashina_list, name='tikuv_mashina_list'),
    path('admin-panel/tikuv-mashinalar/create/', views.tikuv_mashina_create, name='tikuv_mashina_create'),
    path('admin-panel/tikuv-mashinalar/<int:pk>/update/', views.tikuv_mashina_update, name='tikuv_mashina_update'),
    path('admin-panel/tikuv-mashinalar/<int:pk>/delete/', views.tikuv_mashina_delete, name='tikuv_mashina_delete'),
    
    # Main pages
    path('', views.home, name='home'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/create/', views.material_create, name='material_create'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/<int:pk>/update/', views.material_update, name='material_update'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),
    
    # Export
    path('materials/export/excel/', views.export_materials_excel, name='export_materials_excel'),
    path('materials/<int:pk>/pdf/', views.material_pdf, name='material_pdf'),
    
    # Quick actions
    path('materials/<int:pk>/quick-status/', views.material_quick_status, name='material_quick_status'),
    path('mashina-zakazlar/', views.mashina_zakazlar, name='mashina_zakazlar'),
    path('users/', views.user_list, name='user_list'),

    # MaterialType (Material nomlari) CRUD
    path('admin-panel/materialtypes/', views.materialtype_list, name='materialtype_list'),
    path('admin-panel/materialtypes/create/', views.materialtype_create, name='materialtype_create'),
    path('admin-panel/materialtypes/<int:pk>/update/', views.materialtype_update, name='materialtype_update'),
    path('admin-panel/materialtypes/<int:pk>/delete/', views.materialtype_delete, name='materialtype_delete'),

    # Customer (Buyurtmachilar) CRUD
    path('admin-panel/customers/', views.customer_list, name='customer_list'),
    path('admin-panel/customers/create/', views.customer_create, name='customer_create'),
    path('admin-panel/customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('admin-panel/customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    path('materials/<int:pk>/quick-mashina/', views.material_quick_mashina, name='material_quick_mashina'),

    path('admin-panel/mashina-statistika/', views.mashina_statistika, name='mashina_statistika'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Textil API",
      default_version='v1',
      description="Textil materiallari uchun API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('api/materials/', MaterialListCreateAPIView.as_view(), name='api_material_list_create'),
    path('api/materials/<int:pk>/', MaterialRetrieveUpdateDestroyAPIView.as_view(), name='api_material_detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/materials/export/', views.api_export_materials_excel, name='api_export_materials_excel'),
    path('api/materials/<int:pk>/pdf/', views.api_material_pdf, name='api_material_pdf'),
    path('zakazlar/pdf/', views.mashina_zakazlar_pdf, name='mashina_zakazlar_pdf'),
    path('zakazlar/excel/', views.mashina_zakazlar_excel, name='mashina_zakazlar_excel'),
] 