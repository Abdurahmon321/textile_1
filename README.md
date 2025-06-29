# Textil Boshqaruvi Tizimi

Bu Django asosida yaratilgan oddiy textil materiallarini boshqarish tizimi.

## Xususiyatlar

- Materiallar qo'shish, ko'rish, tahrirlash va o'chirish (CRUD)
- Partiya raqami avtomatik generatsiya qilish
- Material statusini kuzatish (Kutish/Tugatildi)
- Vaqt hisobini saqlash
- Chiroyli va qulay interfeys

## O'rnatish

1. Paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

2. Ma'lumotlar bazasini yaratish:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Superuser yaratish:
```bash
python manage.py createsuperuser
```

4. Serverni ishga tushirish:
```bash
python manage.py runserver
```

## Foydalanish

- Bosh sahifa: `http://localhost:8000/`
- Admin panel: `http://localhost:8000/admin/`
- Materiallar ro'yxati: `http://localhost:8000/materials/`

## Model

Material modeli quyidagi maydonlarni o'z ichiga oladi:

- `tikuv_mashina_raqami` - Tikuv mashina raqami
- `partiya_raqami` - Avtomatik generatsiya qilinadigan partiya raqami
- `buyurtmachi` - Buyurtma beruvchi
- `material_rangi` - Material rangi
- `rangi_kodi` - Rangi kodi
- `kilogramm` - Zakaz miqdori (kg)
- `material_nomi` - Material nomi
- `status` - Holat (Kutish/Tugatildi)
- `kiritilgan_vaqt` - Kiritilgan vaqt
- `tugatilgan_vaqt` - Tugatilgan vaqt

## Texnologiyalar

- Django 4.2.7
- Bootstrap 5
- Font Awesome
- SQLite (ma'lumotlar bazasi) 