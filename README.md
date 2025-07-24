# 🏍️ Django فروشگاه آنلاین

یک فروشگاه اینترنتی کامل با استفاده از Django ساخته شده است. این پروژه قابلیت مدیریت محصولات، کاربران، سبد خرید، سفارش‌ها و اتصال به درگاه‌های پرداخت ایرانی را دارد. ساختار پروژه طوری طراحی شده که هم برای توسعه‌دهندگان تازه‌کار و هم حرفه‌ای، قابل توسعه و استفاده در محیط‌های Production باشد.

## 📌 ویژگی‌ها

* احراز هویت کاربران (ورود، ثبت‌نام، خروج)
* ایجاد و مدیریت محصولات با دسته‌بندی
* سیستم جستجو و فیلتر پیشرفته محصولات
* افزودن محصولات به سبد خرید
* ثبت سفارش و پرداخت آنلاین (زرین‌پال / Pay.ir)
* پنل مدیریت برای ادمین‌ها
* طراحی واکنش‌گرا (ریسپانسیو)
* آماده‌سازی برای اتصال به API یا SPA (Django REST Framework)

## ⚙️ تکنولوژی‌ها

* Python 3.11+
* Django 4.x
* SQLite (PostgreSQL برای Production)
* Bootstrap / TailwindCSS
* Pillow
* Celery + Redis (اختیاری)

## 🧹 نصب و اجرا

### 1. کلون کردن پروژه

```bash
git clone https://github.com/mehdi-eti/shop-project.git
cd shop-project
```

### 2. فعالسازی محیط مجازی

```bash
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate
```

### 3. نصب پکیج‌ها

```bash
pip install -r requirements.txt
```

### 4. ساخت فایل .env

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. اجرای مایگریشن و سوپریوزر

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. اجرای سرور

```bash
python manage.py runserver
```

## ✅ TODO

* [ ] اتصال نهایی به درگاه زرین‌پال
* [ ] افزودن نظرات و امتیازدهی
* [ ] افزودن API برای موبایل یا SPA
* [ ] بهینه‌سازی SEO و meta
* [ ] تست‌های coverage مدل‌ها و viewها

## 📁 ساختار پروژه

```
shop-project/
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── ...
├── static/
├── media/
├── db.sqlite3
├── manage.py
├── .env
└── requirements.txt
```

## 📜 لایسنس

انتشار تحت مجوز MIT. فایل LICENSE را ببینید.

## 👤 توسعه‌دهنده

* توسعه‌دهنده: [Mehdi Eti](https://github.com/mehdi-eti)
* GitHub: [github.com/mehdi-eti](https://github.com/mehdi-eti)
