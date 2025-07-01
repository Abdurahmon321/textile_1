from django.contrib import admin
from .models import Material, CustomUser, TikuvMashina, MaterialType, Color, Customer
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.admin import ModelAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_admin', 'is_active', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('username', 'password')
        }),
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Huquqlar', {
            'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Muhim sanalar', {
            'fields': ('last_login', 'date_joined')
        }),
    )

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'faol', 'qo_shilgan_vaqt')
    list_filter = ('faol', 'qo_shilgan_vaqt')
    search_fields = ('nomi', 'tavsif')
    ordering = ('nomi',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'tavsif')
        }),
        ('Holat', {
            'fields': ('faol',)
        }),
        ('Vaqt', {
            'fields': ('qo_shilgan_vaqt',)
        }),
    )

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kodi', 'hex_kodi', 'faol', 'qo_shilgan_vaqt')
    list_filter = ('faol', 'qo_shilgan_vaqt')
    search_fields = ('nomi', 'kodi')
    ordering = ('nomi',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'kodi', 'hex_kodi')
        }),
        ('Holat', {
            'fields': ('faol',)
        }),
        ('Vaqt', {
            'fields': ('qo_shilgan_vaqt',)
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'telefon', 'email', 'faol', 'qo_shilgan_vaqt')
    list_filter = ('faol', 'qo_shilgan_vaqt')
    search_fields = ('nomi', 'telefon', 'email')
    ordering = ('nomi',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'telefon', 'email')
        }),
        ('Manzil va tavsif', {
            'fields': ('manzil', 'tavsif')
        }),
        ('Holat', {
            'fields': ('faol',)
        }),
        ('Vaqt', {
            'fields': ('qo_shilgan_vaqt',)
        }),
    )

@admin.register(TikuvMashina)
class TikuvMashinaAdmin(admin.ModelAdmin):
    list_display = ('raqami', 'nomi', 'holati', 'qo_shilgan_vaqt')
    list_filter = ('holati', 'qo_shilgan_vaqt')
    search_fields = ('raqami', 'nomi')
    ordering = ('raqami',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('raqami', 'nomi')
        }),
        ('Holat', {
            'fields': ('holati',)
        }),
        ('Vaqt', {
            'fields': ('qo_shilgan_vaqt',)
        }),
    )

class MaterialAdmin(SimpleHistoryAdmin):
    list_display = ('partiya_raqami', 'tikuv_mashina', 'buyurtmachi', 'material_turi', 'material_rangi', 'status', 'kiritilgan_vaqt', 'created_by')
    list_filter = ('status', 'kiritilgan_vaqt', 'material_gramaji_turi', 'tikuv_mashina', 'material_turi', 'tup_aen_turi', 'ribana_kashkor_turi', 'bayka_turi')
    search_fields = ('partiya_raqami', 'buyurtmachi__nomi', 'material_turi__nomi', 'material_rangi')
    ordering = ('-kiritilgan_vaqt',)
    readonly_fields = ('partiya_raqami', 'kiritilgan_vaqt', 'created_by')
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('partiya_raqami', 'tikuv_mashina', 'buyurtmachi')
        }),
        ('Material ma\'lumotlari', {
            'fields': ('material_turi', 'material_rangi', 'material_gramaji_turi', 'material_gramaji', 'kilogramm')
        }),
        ('Qo\'shimcha materiallar', {
            'fields': ('ribana_kashkor_turi', 'ribana_kashkor_kg', 'bayka_turi', 'bayka_kg', 'tup_aen_turi'),
            'classes': ('collapse',)
        }),
        ('Status va vaqt', {
            'fields': ('status', 'kiritilgan_vaqt', 'tugatilgan_vaqt')
        }),
        ('Qo\'shimcha', {
            'fields': ('created_by',)
        }),
    )
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Material, MaterialAdmin)

class LogEntryAdmin(ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['user', 'content_type', 'action_flag']
    search_fields = ['object_repr', 'change_message']

admin.site.register(LogEntry, LogEntryAdmin) 