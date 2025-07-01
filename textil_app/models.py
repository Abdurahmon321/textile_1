from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import random
from datetime import timedelta
from simple_history.models import HistoricalRecords

def generate_partiya_raqami():
    return str(random.randint(10000, 99999))

STATUS_CHOICES = [
    ('waiting', 'Kutish'),
    ('progress', 'Jarayonda'),
    ('completed', 'Tugatilgan'),
]

GRAMMAJ_CHOICES = [
    ('sm', 'Santimetr (sm)'),
    ('gram', 'Gramm (g)'),
]

TUP_AEN_CHOICES = [
    ('tup', 'Tup'),
    ('aen', 'AEN'),
]

RIBANA_KASHKOR_CHOICES = [
    ('ribana', 'Ribana'),
    ('kashkor', 'Kashkor'),
]

BAYKA_CHOICES = [
    ('bayka', 'Bayka'),
]

class CustomUser(AbstractUser):
    """Foydalanuvchi modeli"""
    is_admin = models.BooleanField("Admin", default=False)
    phone = models.CharField("Telefon raqam", max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class MaterialType(models.Model):
    """Material turi modeli"""
    nomi = models.CharField("Material nomi", max_length=100, unique=True)
    tavsif = models.TextField("Tavsif", blank=True, null=True)
    qo_shilgan_vaqt = models.DateTimeField("Qo'shilgan vaqt", default=timezone.now)
    faol = models.BooleanField("Faol", default=True)
    
    def __str__(self):
        return self.nomi
    
    class Meta:
        verbose_name = "Material turi"
        verbose_name_plural = "Material turlari"
        ordering = ['nomi']

class Color(models.Model):
    """Rang modeli"""
    nomi = models.CharField("Rang nomi", max_length=50, unique=True)
    kodi = models.CharField("Rang kodi", max_length=20, blank=True, null=True)
    hex_kodi = models.CharField("Hex kodi", max_length=7, blank=True, null=True, help_text="Masalan: #FF0000")
    qo_shilgan_vaqt = models.DateTimeField("Qo'shilgan vaqt", default=timezone.now)
    faol = models.BooleanField("Faol", default=True)
    
    def __str__(self):
        if self.kodi:
            return f"{self.nomi} ({self.kodi})"
        return self.nomi
    
    class Meta:
        verbose_name = "Rang"
        verbose_name_plural = "Ranglar"
        ordering = ['nomi']

class Customer(models.Model):
    """Buyurtmachi modeli"""
    nomi = models.CharField("Buyurtmachi nomi", max_length=100)
    telefon = models.CharField("Telefon raqam", max_length=15, blank=True, null=True)
    manzil = models.TextField("Manzil", blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    tavsif = models.TextField("Qo'shimcha ma'lumot", blank=True, null=True)
    qo_shilgan_vaqt = models.DateTimeField("Qo'shilgan vaqt", default=timezone.now)
    faol = models.BooleanField("Faol", default=True)
    
    def __str__(self):
        return self.nomi
    
    class Meta:
        verbose_name = "Buyurtmachi"
        verbose_name_plural = "Buyurtmachilar"
        ordering = ['nomi']

class TikuvMashina(models.Model):
    """Tikuv mashina modeli"""
    raqami = models.CharField("Mashina raqami", max_length=20, unique=True)
    nomi = models.CharField("Mashina nomi", max_length=100, blank=True, null=True)
    holati = models.CharField("Holati", max_length=20, choices=[
        ('active', 'Faol'),
        ('inactive', 'Faol emas'),
        ('repair', 'Ta\'mirlanmoqda'),
    ], default='active')
    qo_shilgan_vaqt = models.DateTimeField("Qo'shilgan vaqt", default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.raqami:
            # Eng katta raqamni topamiz
            oxirgi = TikuvMashina.objects.order_by('-id').first()
            if oxirgi and oxirgi.raqami.isdigit():
                self.raqami = str(int(oxirgi.raqami) + 1)
            else:
                self.raqami = '1'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.raqami} - {self.nomi or 'Nomsiz'}"
    
    class Meta:
        verbose_name = "To'quv mashina"
        verbose_name_plural = "To'quv mashinalari"

class Material(models.Model):
    tikuv_mashina = models.ForeignKey(TikuvMashina, on_delete=models.CASCADE, verbose_name="Tikuv mashina")
    partiya_raqami = models.PositiveIntegerField("Partiya raqami", unique=True, blank=True, null=True)
    buyurtmachi = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Buyurtmachi")
    material_turi = models.ForeignKey(MaterialType, on_delete=models.CASCADE, verbose_name="Material turi")
    material_rangi = models.CharField("Material rangi", max_length=100, help_text="Material rangini kiriting")
    material_gramaji_turi = models.CharField("Material gramaji turi", max_length=4, choices=GRAMMAJ_CHOICES, default='sm')
    material_gramaji = models.DecimalField("Material gramaji", max_digits=10, decimal_places=2, default=0.00)
    kilogramm = models.DecimalField("Zakaz (kg)", max_digits=10, decimal_places=2)
    
    # Yangi maydonlar
    ribana_kashkor_turi = models.CharField("Ribana/Kashkor turi", max_length=10, choices=RIBANA_KASHKOR_CHOICES, null=True, blank=True, help_text="Ribana yoki Kashkor tanlang")
    ribana_kashkor_kg = models.DecimalField("Ribana/Kashkor (kg)", max_digits=10, decimal_places=2, null=True, blank=True, help_text="Ribana yoki Kashkor tanlangan bo'lsa kg kiritish zarur")
    bayka_turi = models.CharField("Bayka turi", max_length=10, choices=BAYKA_CHOICES, null=True, blank=True, help_text="Bayka tanlang")
    bayka_kg = models.DecimalField("Bayka (kg)", max_digits=10, decimal_places=2, null=True, blank=True, help_text="Bayka tanlangan bo'lsa kg kiritish zarur")
    tup_aen_turi = models.CharField("Tup/AEN turi", max_length=3, choices=TUP_AEN_CHOICES, null=True, blank=True, help_text="Tup yoki AEN tanlash (majburiy emas)")
    
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='waiting')
    kiritilgan_vaqt = models.DateTimeField("Kutishga qo'yilgan vaqt", default=timezone.now)
    tugatilgan_vaqt = models.DateTimeField("Tugatildi vaqti", null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Qo'shgan foydalanuvchi")
    history = HistoricalRecords()
    izoh = models.TextField("Izoh", blank=True, null=True, help_text="Qo'shimcha izoh yoki eslatma")

    def save(self, *args, **kwargs):
        if not self.pk and not self.partiya_raqami:
            # Eng katta partiya raqamini topamiz
            oxirgi = Material.objects.order_by('-partiya_raqami').first()
            if oxirgi and oxirgi.partiya_raqami:
                self.partiya_raqami = oxirgi.partiya_raqami + 1
            else:
                self.partiya_raqami = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.partiya_raqami} - {self.buyurtmachi.nomi}"

    @property
    def qancha_vaqt_olgan(self):
        if self.status == 'completed' and self.tugatilgan_vaqt:
            return self.tugatilgan_vaqt - self.kiritilgan_vaqt
        return None

    @property
    def qancha_soat_olgan(self):
        if self.qancha_vaqt_olgan:
            total_seconds = self.qancha_vaqt_olgan.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours} soat {minutes} daqiqa"
        return ""
    
    @property
    def material_gramaji_ko_rsatish(self):
        """Material gramajini ko'rsatish"""
        return f"{self.material_gramaji} {self.get_material_gramaji_turi_display()}"
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
        ordering = ['-kiritilgan_vaqt'] 