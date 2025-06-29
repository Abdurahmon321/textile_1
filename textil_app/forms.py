from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Material, CustomUser, TikuvMashina, MaterialType, Color, Customer
import re

class MaterialTypeForm(forms.ModelForm):
    class Meta:
        model = MaterialType
        fields = ['nomi', 'tavsif', 'faol']
        widgets = {
            'nomi': forms.TextInput(attrs={'class': 'form-control'}),
            'tavsif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'faol': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['nomi', 'kodi', 'hex_kodi', 'faol']
        widgets = {
            'nomi': forms.TextInput(attrs={'class': 'form-control'}),
            'kodi': forms.TextInput(attrs={'class': 'form-control'}),
            'hex_kodi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#FF0000'}),
            'faol': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_hex_kodi(self):
        hex_kodi = self.cleaned_data.get('hex_kodi')
        if hex_kodi and not re.match(r'^#[0-9A-Fa-f]{6}$', hex_kodi):
            raise forms.ValidationError("Hex kodi to'g'ri formatda bo'lishi kerak (masalan: #FF0000)")
        return hex_kodi

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['nomi', 'telefon', 'manzil', 'email', 'tavsif', 'faol']
        widgets = {
            'nomi': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}),
            'manzil': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tavsif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'faol': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if telefon:
            # Telefon raqamini tozalash
            telefon = re.sub(r'[^\d+]', '', telefon)
            if not re.match(r'^\+?998?\d{9}$', telefon):
                raise forms.ValidationError("Telefon raqam to'g'ri formatda bo'lishi kerak")
        return telefon

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['tikuv_mashina', 'buyurtmachi', 'material_turi', 'material_rangi', 'material_gramaji_turi', 'material_gramaji', 'kilogramm', 'status']
        widgets = {
            'tikuv_mashina': forms.Select(attrs={'class': 'form-control select2'}),
            'buyurtmachi': forms.Select(attrs={'class': 'form-control select2'}),
            'material_turi': forms.Select(attrs={'class': 'form-control select2'}),
            'material_rangi': forms.Select(attrs={'class': 'form-control select2'}),
            'material_gramaji_turi': forms.Select(attrs={'class': 'form-control select2'}),
            'material_gramaji': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'kilogramm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat faol buyurtmachilar va material turlarini ko'rsatish
        self.fields['buyurtmachi'].queryset = Customer.objects.filter(faol=True)
        self.fields['material_turi'].queryset = MaterialType.objects.filter(faol=True)
        self.fields['material_rangi'].queryset = Color.objects.filter(faol=True)
        
        # Majburiy maydonlarni belgilash
        self.fields['tikuv_mashina'].required = True
        self.fields['buyurtmachi'].required = True
        self.fields['material_turi'].required = True
        self.fields['material_rangi'].required = True
        self.fields['kilogramm'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        print(f"Cleaned data: {cleaned_data}")  # Debug
        
        # Majburiy maydonlarni tekshirish
        required_fields = ['tikuv_mashina', 'buyurtmachi', 'material_turi', 'material_rangi', 'kilogramm']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"Bu maydon majburiy.")
        
        # Kilogramm musbat bo'lishi kerak
        kilogramm = cleaned_data.get('kilogramm')
        
        if kilogramm is not None and kilogramm <= 0:
            self.add_error('kilogramm', "Kilogramm 0 dan katta bo'lishi kerak.")
        
        return cleaned_data

class TikuvMashinaForm(forms.ModelForm):
    class Meta:
        model = TikuvMashina
        fields = ['nomi', 'holati']
        widgets = {
            'nomi': forms.TextInput(attrs={'class': 'form-control'}),
            'holati': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    """Foydalanuvchi qo'shish formasi"""
    is_admin = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Admin huquqlari"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'is_admin', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            # Kamida 8 belgi
            if len(password) < 8:
                raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
            
            # Harf va raqam bo'lishi kerak
            if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
                raise forms.ValidationError("Parol harflar va raqamlardan iborat bo'lishi kerak.")
        
        return password

class CustomAuthenticationForm(AuthenticationForm):
    """Login formasi"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    ) 