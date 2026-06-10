"""
ملف حقن البيانات (Seed Data) للمشروع
يجب تشغيله بعد تطبيق الـ migrations
الأمر: python manage.py shell < seed_data.py
"""

import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')  # غيّر config لاسم مجلد الـ settings عندك
django.setup()

from decimal import Decimal
from datetime import date, time

from patients.models import Patient
from users.models import User
from notifications.models import Notification
from nutritionists.models import Product, Nutritionist
from publications.models import EducationalPublication
from subscriptions.models import Workshop
# ========== USERS & PATIENTS ==========

def create_users_and_patients():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    patients_data = [
        {
            "username": "hnadihasan",
            "email": "hnadihasan@gmail.com",
            "first_name": "هنادي",
            "last_name": "محمد حسن",
            "phone": "0954238459",
            "birth_date": date(2004, 5, 20),
            "gender": "female",
            "address": "طرطوس صافيتا",
        },
        {
            "username": "hadeela12",
            "email": "hadeela12@gmail.com",
            "first_name": "هديل",
            "last_name": "عبد الكريم",
            "phone": "+963988555444",
            "birth_date": date(2001, 4, 21),
            "gender": "female",
            "address": "سوريا - حمص - الأهرام",
        },
        {
            "username": "tasnimmohammad",
            "email": "tasnimmohammad@gmail.com",
            "first_name": "تسنيم",
            "last_name": "عبدالرحمن محمد",
            "phone": "0975458258",
            "birth_date": date(1999, 7, 5),
            "gender": "female",
            "address": "حماه – ساحة العاصي",
        },
        {
            "username": "ahmadmahmoud",
            "email": "ahmadmahmoud@gmail.com",
            "first_name": "احمد",
            "last_name": "محمد محمود",
            "phone": "0945785327",
            "birth_date": date(2000, 9, 22),
            "gender": "male",
            "address": "حمص - الحضارة",
        },
        {
            "username": "mohammadhasoun",
            "email": "mohammadhasoun@gmail.com",
            "first_name": "محمد",
            "last_name": "عبد العزيز حسون",
            "phone": "0984526741",
            "birth_date": date(1995, 7, 23),
            "gender": "male",
            "address": "دمشق - بلودان",
        },
    ]


    created_patients = []
    for data in patients_data:
        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={
                "username": data["username"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "phone": data["phone"],
                "birth_date": data["birth_date"],
                "gender": data["gender"],
                "address": data["address"],
                "is_verified": True,
                "status": "active",
            }
        )
        if created:
            user.set_password("Patient@123")
            user.save()

        patient, _ = Patient.objects.get_or_create(user=user)
        created_patients.append(patient)
        print(f"✅ Patient: {user.get_full_name()}")

    return created_patients


# ========== PACKAGES ==========

def create_packages(nutritionist):
    from subscriptions.models import Package  # ← غيّر your_app لاسم تطبيقك

    packages_data = [
        # --- اشتراكات التغذية ---
        {
            "name": "باقة العافية",
            "details": "لدعم عافية الجسد وعلاج المشاكل الصحية والأمراض\n- جلسة استشارة\n- دراسة حالة\n- حمية علاجية\n- جلسة متابعة وتقييم\n- متابعة واتساب أسبوعية",
            "price": Decimal("35.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": None,
        },
        {
            "name": "اشتراك حياة جديدة",
            "details": "لتعديل السلوكيات الغذائية وتبني نمط حياة صحي\n- جلسة استشارة\n- خريطة التغيير\n- خطة غذائية\n- وصفات صحية\n- بنك الصحة\n- جلسة تقييم",
            "price": Decimal("50.00"),
            "num": 1,
            "category": "diet",
            "require_consultation": True,
            "first_payment_percentage": None,
        },
        {
            "name": "رحلة الميزان",
            "details": "لتعديل وإدارة الوزن وموازنة كتلة الدهون والعضل ونسبة الماء بالجسم\n- جلسة استشارة\n- تحليل INBODY\n- 1-2 برنامج غذائي\n- جلسة متابعة\n- متابعة واتساب أسبوعية",
            "price": Decimal("27.50"),  # متوسط 25-30
            "num": 1,
            "category": "diet",
            "require_consultation": True,
            "first_payment_percentage": None,
        },
        {
            "name": "اشتراك 7 نجوم",
            "details": "- جلسة استشارة\n- تحليل INBODY ودراسة حالة\n- خطة غذائية\n- تمارين رياضية\n- جلسة متابعة وتقييم\n- جلسة تثقيف ودعم سلوكي\n- متابعة واتساب أسبوعية",
            "price": Decimal("125.00"),  # متوسط 100-150
            "num": 1,
            "category": "diet",
            "require_consultation": True,
            "first_payment_percentage": None,
        },
        # --- باقات الأجهزة ---
        {
            "name": "باقة السعادة",
            "details": "تقنيات التنحيف وأجهزة تحسين القوام\n- 1 كرايو\n- 4 كافيتيشن + RF\n- 4 EMS\n- 1 تصريف لمفاوي\n(10 جلسات)",
            "price": Decimal("200.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": False,
            "first_payment_percentage": None,
        },
        {
            "name": "باقة القوة والشباب",
            "details": "لتحفيز العضلات ورفع معدل الاستقلاب\n- 8 جلسات EMS\n- 2 جلسة تصريف لمفاوي\n(10 جلسات)",
            "price": Decimal("150.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": False,
            "first_payment_percentage": None,
        },
        {
            "name": "باقة REFRESH",
            "details": "بعد رحلة الحمل والولادة وعمليات القيصرية\n- 6 جلسات EMS\n- 3 جلسات RF/كافيتيشن\n- 1 جلسة تصريف لمفاوي\n(10 جلسات)",
            "price": Decimal("170.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": False,
            "first_payment_percentage": None,
        },
        {
            "name": "باقة الجمال والدلال",
            "details": "- 6 جلسات كافيتيشن/RF\n- 2 جلسة تصريف لمفاوي\n- 2 جلسة EMS/ليزر بادز\n(10 جلسات)",
            "price": Decimal("150.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": False,
            "first_payment_percentage": None,
        },
        # --- الحقونات ---
        {
            "name": "كورس أبر مونجارو/أوزمبك - شهر",
            "details": "رحلة تنزيل الوزن مع أبر مونجارو - أوزمبك\n- 4 أبر أسبوعية\n- خطة متكاملة (تغذية + سلوكيات داعمة)\n- خطة المتابعة والتقييم\n- INBODY",
            "price": Decimal("350.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("28.57"),  # 100/350
        },
        {
            "name": "كورس أبر مونجارو/أوزمبك مع أجهزة - شهر",
            "details": "كورس أبر مع كورس أجهزة 10 جلسات\n- 4 أبر أسبوعية\n- خطة متكاملة (تغذية + سلوكيات داعمة)\n- 10 جلسات أجهزة",
            "price": Decimal("400.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("37.50"),  # 150/400
        },
        {
            "name": "كورس أبر مونجارو/أوزمبك - 3 أشهر",
            "details": "- 12 أبرة\n- خطة متكاملة (تغذية + سلوكيات داعمة)\n- خطة المتابعة والتقييم\n- INBODY شهرياً\nجدول الدفع: دفعة أولى 100$ - دفعة 2: 300$ - دفعة 3: 300$ - دفعة 4: 200$",
            "price": Decimal("900.00"),
            "num": 3,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("11.11"),  # 100/900
        },
        {
            "name": "كورس أبر مونجارو/أوزمبك مع أجهزة - 3 أشهر",
            "details": "كورس أبر 3 أشهر مع كورس أجهزة\n- 12 أبرة + جلسات أجهزة\n- خطة متكاملة شاملة\nجدول الدفع: دفعة أولى + 4 دفعات تقسيط",
            "price": Decimal("1300.00"),
            "num": 3,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("7.69"),
        },
        {
            "name": "كورس أبر مونجارو/أوزمبك - 6 أشهر",
            "details": "- 24 أبرة\n- خطة متكاملة (تغذية + سلوكيات داعمة)\n- خطة المتابعة والتقييم\n- INBODY شهرياً\nجدول الدفع: دفعة أولى 300$ - دفعة 2: 400$ - دفعة 3: 500$ - دفعة 4: 500$",
            "price": Decimal("1700.00"),
            "num": 6,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("17.65"),  # 300/1700
        },
        {
            "name": "كورس أبر مونجارو/أوزمبك مع أجهزة - 6 أشهر",
            "details": "كورس أبر 6 أشهر مع أجهزة\n- 24 أبرة + جلسات أجهزة\n- خطة متكاملة شاملة\n- INBODY شهرياً",
            "price": Decimal("2300.00"),
            "num": 6,
            "category": "medical",
            "require_consultation": True,
            "first_payment_percentage": Decimal("13.04"),
        },
        {
            "name": "أبر إذابة الدهون الموضعية",
            "details": "- 10ml أبر إذابة دهون\n- جلسة كافيتيشن\n- جلسة تصريف لمفاوي\n- نصائح غذائية",
            "price": Decimal("150.00"),
            "num": 1,
            "category": "medical",
            "require_consultation": False,
            "first_payment_percentage": None,
        },
    ]

    for data in packages_data:
        pkg, created = Package.objects.get_or_create(
            name=data["name"],
            nutritionist=nutritionist,
            defaults={
                "details": data["details"],
                "price": data["price"],
                "num": data["num"],
                "category": data["category"],
                "require_consultation": data["require_consultation"],
                "first_payment_percentage": data["first_payment_percentage"],
                "status": True,
            }
        )
        print(f"{'✅' if created else '⚠️ exists'} Package: {data['name']}")


# ========== PRODUCTS ==========

def create_products(nutritionist):

    products_data = [
        {"name": "مستحضرات تجميل / كريمات للعناية بالبشرة", "price": Decimal("15.00"), "quantity": 23, "type": "herbal"},
        {"name": "علبة منتج عناية",                           "price": Decimal("15.00"), "quantity": 54, "type": "herbal"},
        {"name": "Dumbbell",                                   "price": Decimal("8.00"),  "quantity": 3,  "type": "tools"},
        {"name": "مطرة ماء رياضية",                           "price": Decimal("5.00"),  "quantity": 52, "type": "tools"},
        {"name": "عبوة بخاخ",                                  "price": Decimal("8.00"),  "quantity": 83, "type": "herbal"},
        {"name": "كوب / فنجان صغير",                          "price": Decimal("15.00"), "quantity": 14, "type": "tools"},
        {"name": "علبة بلاستيكية لحفظ الطعام",                "price": Decimal("15.00"), "quantity": 3,  "type": "tools"},
        {"name": "عبوة منتج عناية شخصية",                     "price": Decimal("5.00"),  "quantity": 23, "type": "herbal"},
        {"name": "مجموعة مكيال للطعام",                       "price": Decimal("10.00"), "quantity": 8,  "type": "tools"},
        {"name": "كوب بلاستيكي شفاف للعصائر",                 "price": Decimal("2.00"),  "quantity": 11, "type": "snacks"},
        {"name": "لانش بوكس",                                  "price": Decimal("3.00"),  "quantity": 3,  "type": "tools"},
        {"name": "Note Book",                                  "price": Decimal("1.00"),  "quantity": 25, "type": "tools"},
    ]

    for data in products_data:
        prod, created = Product.objects.get_or_create(
            name=data["name"],
            nutritionist=nutritionist,
            defaults={
                "price": data["price"],
                "quantity": data["quantity"],
                "type": data["type"],
                "is_available": True,
                # img: متجاهَل حسب التعليمات
            }
        )
        print(f"{'✅' if created else '⚠️ exists'} Product: {data['name']}")


# ========== EDUCATIONAL PUBLICATIONS ==========

def create_publications(nutritionist):

    publications_data = [
        {
            "title": "عجلة المشاعر والأكل العاطفي",
            "overview": "هل بتاكل لأنك جوعان… ولا لأنك متضايق؟",
            "content": (
                "أحيانًا ما نكون محتاجين أكل، بل محتاجين: راحة، أمان، تفريغ مشاعر.\n\n"
                "عجلة المشاعر بتورجينا إنو:\n"
                "الحزن → أكل سكريات\n"
                "التوتر → أكل سريع\n"
                "الملل → بلع بدون وعي\n\n"
                "المشكلة مو بالأكل… المشكلة إنو الأكل صار الطريقة الوحيدة للتعامل مع المشاعر.\n\n"
                "خطوة تغيير بسيطة: بلحظة الشهية الانفعالية قبل ما تاكل اسأل نفسك:\n"
                "شو الشعور اللي حاسس فيه هلأ؟\n"
                "إذا عرفت الشعور، نص الحل صار موجود."
            ),
            "last_sentence": "عافية وسلام – لأن صحتك النفسية أساس تغذيتك.",
            "status": "published",
        },
        {
            "title": "مقياس الجوع والشبع (الأكل بوعي)",
            "overview": "كم مرة أكلنا لأنو صار وقت الأكل مو لأنو جوعانين؟",
            "content": (
                "مقياس الجوع والشبع بيساعدنا نرجّع الثقة بإشارات جسمنا.\n\n"
                "تخيّل مقياس من 1 لـ 10:\n"
                "1 = جوع شديد وتعب\n"
                "5 = جوع معتدل ومريح\n"
                "7 = شبع مريح\n"
                "10 = امتلاء مزعج\n\n"
                "الهدف مو نوصل للجوع الشديد، ولا نكمّل الأكل لحدّ التخمة.\n"
                "أفضل مكان نبدأ فيه الأكل: 3–4\n"
                "أفضل مكان نوقف فيه: 6–7\n\n"
                "لما نسمع لجسمنا:\n"
                "الهضم بيكون أفضل\n"
                "نوبات الأكل العاطفي بتخف\n"
                "علاقتنا مع الأكل بتتحسن\n\n"
                "الأكل بوعي مو حرمان… هو احترام لإشارات جسمك."
            ),
            "last_sentence": "عافية وسلام – نعلّمك تسمع لجسمك، مو تحاربه.",
            "status": "published",
        },
    ]

    for data in publications_data:
        pub, created = EducationalPublication.objects.get_or_create(
            title=data["title"],
            nutritionist=nutritionist,
            defaults={
                "overview": data["overview"],
                "content": data["content"],
                "last_sentence": data["last_sentence"],
                "status": data["status"],
            }
        )
        print(f"{'✅' if created else '⚠️ exists'} Publication: {data['title']}")


# ========== WORKSHOPS ==========

def create_workshops(nutritionist):

    workshops_data = [
        {
            "title": "تحاليل الـ INBODY",
            "date": date(2025, 6, 15),  # ← عدّل التاريخ حسب الحاجة
            "time": time(10, 0),
            "place": "",
            "type": "online",
            "overview": (
                "ورشة تدريبية لشرح تحاليل الـ INBODY لقياس مكونات الجسم:\n"
                "دهون - عضلات - ماء - عظام - العمر البيولوجي - نسبة الاستقلاب - "
                "توزع الدهون والعضلات - نمط الجسم الصحي"
            ),
            "link": "http://trywithus",
            "status": "upcoming",
            "max_participants": 50,
        },
    ]

    for data in workshops_data:
        ws, created = Workshop.objects.get_or_create(
            title=data["title"],
            nutritionist=nutritionist,
            defaults={
                "date": data["date"],
                "time": data["time"],
                "place": data["place"],
                "type": data["type"],
                "overview": data["overview"],
                "link": data["link"],
                "status": data["status"],
                "max_participants": data["max_participants"],
            }
        )
        print(f"{'✅' if created else '⚠️ exists'} Workshop: {data['title']}")


# ========== NOTIFICATIONS ==========

def create_notifications(patients):

    # patients[0] = هنادي، patients[1] = هديل، وهكذا
    notifications_data = [
        {
            "patient": patients[3],  # احمد محمد محمود
            "title": "تم حجز موعد جديد",
            "info": "قام العميل أحمد محمد بحجز موعد جديد يوم الثلاثاء الساعة 10:00 ص",
            "status": "unread",
        },
        {
            "patient": patients[0],  # هنادي
            "title": "تنبيه مخزون منخفض",
            "info": "وصل المنتج ENERGY BAR إلى الحد الأدنى للمخزون (5 قطع متبقية)",
            "status": "unread",
        },
        {
            "patient": patients[2],  # تسنيم
            "title": "تذكير بجلسة غذائية",
            "info": "موعد جلسة متابعة للمريضة علي حسن يبدأ بعد 30 دقيقة من الآن",
            "status": "unread",
        },
        {
            "patient": patients[1],  # هديل
            "title": "إضافة منتج للسلة",
            "info": "تم إضافة لانش بوكس إلى سلة التسوق الخاصة بالمريضة سارة العبداللة",
            "status": "unread",
        },
        {
            "patient": patients[4],  # محمد عبد العزيز
            "title": "تم حجز موعد جديد",
            "info": "قام العميل أحمد خالد بحجز موعد جديد",
            "status": "unread",
        },
    ]

    for data in notifications_data:
        notif = Notification.objects.create(
            patient=data["patient"],
            title=data["title"],
            info=data["info"],
            status=data["status"],
        )
        print(f"✅ Notification: {data['title']} → {data['patient'].user.get_full_name()}")


# ========== MAIN ==========

def run():
    print("\n" + "="*50)
    print("🚀 بدء حقن البيانات")
    print("="*50)

    # تأكد من وجود Nutritionist في قاعدة البيانات أولاً
    # يمكنك تغيير هذا السطر حسب طريقة إنشاء الـ Nutritionist عندك
    nutritionist = Nutritionist.objects.first()
    if not nutritionist:
        print("❌ لا يوجد Nutritionist في قاعدة البيانات. أضف واحداً أولاً.")
        return

    print(f"\n📋 استخدام أخصائي التغذية: {nutritionist}")

    print("\n--- Users & Patients ---")
    patients = create_users_and_patients()

    print("\n--- Packages ---")
    create_packages(nutritionist)

    print("\n--- Products ---")
    create_products(nutritionist)

    print("\n--- Educational Publications ---")
    create_publications(nutritionist)

    print("\n--- Workshops ---")
    create_workshops(nutritionist)

    print("\n--- Notifications ---")
    create_notifications(patients)

    print("\n" + "="*50)
    print("✅ اكتمل حقن البيانات بنجاح!")
    print("="*50 + "\n")


run()