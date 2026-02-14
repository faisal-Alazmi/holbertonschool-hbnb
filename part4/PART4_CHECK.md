# Part 4 – فحص وتأكيد

## الملفات والبنية
- **index.html** – قائمة الأماكن (Places)، تحويل لـ login إذا لا يوجد توكن
- **login.html** – تسجيل الدخول، الصفحة الأولى عند فتح `/`
- **place.html** – تفاصيل مكان + رابط إضافة مراجعة
- **add_review.html** – نموذج إضافة مراجعة (يحتاج place_id في الرابط)
- **scripts.js** – كل المنطق (دخول، خروج، جلب أماكن، تفاصيل، مراجعات)
- **styles.css** – التنسيق (الكلاسات المطلوبة: logo, login-button, place-card, details-button, place-details, place-info, review-card, add-review, form)
- **server.py** – سيرفر محلي بورت 8000 + بروكسي `/api/*` إلى Part 3 (5000)
- **images/** – logo.png, place_placeholder.svg, wifi.png, bed.png, bathtub.png

## التدفق
1. فتح `http://127.0.0.1:8000/` → عرض **login.html**
2. تسجيل الدخول (مثلاً admin@example.com / admin123) → تحويل إلى **index.html** (Places)
3. في index: عرض تسجيل خروج، إخفاء تسجيل الدخول، جلب الأماكن وعرضها
4. الضغط على "View Details" → **place.html?id=...** (تفاصيل + مراجعات)
5. إذا مسجّل دخول: يظهر "Add a Review" → **add_review.html?place_id=...**
6. إرسال المراجعة → POST /api/v1/reviews/ مع توكن

## ما تم إصلاحه أثناء الفحص
- إزالة `return { ok: true };` غير القابل للوصول في `loginUser`
- عند فتح add_review بدون توكن: التحويل إلى **login.html** بدل index

## تشغيل Part 4
1. Part 3 يعمل: `cd part3` ثم `python run.py` (بورت 5000)
2. Part 4: `cd part4` ثم `python server.py` (بورت 8000)
3. المتصفح: `http://127.0.0.1:8000/`

## الـ API المستخدمة (عبر البروكسي)
- `GET /api/v1/places/` – قائمة الأماكن
- `GET /api/v1/places/<id>` – تفاصيل مكان
- `GET /api/v1/reviews/` – كل المراجعات (يتم فلترتها حسب place_id في الواجهة)
- `POST /api/v1/auth/login` – تسجيل الدخول (email, password)
- `POST /api/v1/reviews/` – إضافة مراجعة (نص، تقييم، user_id من التوكن، place_id)

تم التأكد من Part 4 وتشغيله كما هو متوقع.
