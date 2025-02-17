import re
from django.db import connection, models
from django.apps import apps

def IsnationalCode(text):
    if len(text) == 11 and text.startswith('9'):
        text = text[1:]
        print('text>>>>>>>>:', text)
    # Your existing IsnationalCode function
    
    if len(text) != 10:
        return False
    if text in ['0000000000', '1111111111', '2222222222', '3333333333', 
                 '4444444444', '5555555555', '6666666666', '7777777777', 
                 '8888888888', '9999999999']:
        return False
    
    n = sum(int(text[i]) * (10 - i) for i in range(9))
    lastChar = int(text[9])
    remain = n % 11
    if (remain == 0 and remain == lastChar) or (remain == 1 and remain == lastChar) or (remain > 1 and 11 - remain == lastChar):
        return True

    return False




# لیست پیش‌شماره‌های معتبر اپراتورهای ایران
VALID_PREFIXES = {
    "همراه اول": ["0910", "0911", "0912", "0913", "0914", "0915", "0916", "0917", "0918", "0919", "0990", "0991", "0992"],
    "ایرانسل": ["0901", "0902", "0903", "0904", "0905", "0930", "0933", "0935", "0936", "0937", "0938", "0939", "0993", "0994"],
    "رایتل": ["0920", "0921", "0922"],
    "شاتل موبایل": ["0998"],
    "سامانتل": ["0999"],
    "آپتل": ["0994"]
}

def is_valid_iranian_mobile(number):
    """ بررسی می‌کند که آیا شماره موبایل ایرانی معتبر است یا نه """
    # بررسی اینکه شماره شامل فقط اعداد باشد
    if not re.fullmatch(r"\d{11}", number):
        return False, "شماره باید ۱۱ رقم و فقط شامل اعداد باشد."
    
    # بررسی اینکه شماره با 09 شروع شود
    if not number.startswith("09"):
        return False, "شماره باید با 09 شروع شود."

    # بررسی پیش‌شماره معتبر
    prefix = number[:4]
    for operator, prefixes in VALID_PREFIXES.items():
        if prefix in prefixes:
            return True, f"شماره معتبر است و متعلق به اپراتور {operator}."

    return False, "پیش‌شماره نامعتبر است."

def validate_iranian_cardnumber(iranian_cardnumber):
    # Step 1: Check if the length of the card number is 10 digits
    if len(iranian_cardnumber) != 16 or not iranian_cardnumber.isdigit():
        return False
    
    # Step 2: Check if the first digit is a valid card type
    digits = [int(x) for x in iranian_cardnumber][::-1]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def get_existing_columns(table_name):
    with connection.cursor() as cursor:
        query = f"PRAGMA table_info('{table_name}')"
        cursor.execute(query)
        return {row[1] for row in cursor.fetchall()}
    

def add_missing_columns(table_name, fields):
    existing_columns = get_existing_columns(table_name)

    with connection.cursor() as cursor:
        for field in fields:
            if field.name not in existing_columns:
                query = f'ALTER TABLE "{table_name}" ADD COLUMN "{field.name}" {field.type}'
                cursor.execute(query)


def create_table(table_name, fields):
    # if table_exists(table_name):
    #     # اگر جدول وجود دارد، فقط ستون‌های جدید را اضافه کن
    #     add_missing_columns(table_name, fields)
    #     return

    # ایجاد جدول جدید در صورت عدم وجود
    field_definitions = ", ".join([f'"{field.name}" {field.type}' for field in fields])
    query = f'CREATE TABLE "{table_name}" (id INTEGER PRIMARY KEY, {field_definitions})'
    
    with connection.cursor() as cursor:
        cursor.execute(query)


def database_table_exists(table_name):
    """بررسی می‌کند که آیا جدول موردنظر در دیتابیس وجود دارد یا نه"""
    return table_name in connection.introspection.table_names()


#for other databases
# def create_table(table_name, fields):
#     """ایجاد یک مدل داینامیک برای جدول جدید"""
    
#     # اگر جدول از قبل وجود دارد، متوقف شود
#     # if database_table_exists(table_name):
#     #     return  

#     # تعریف دیکشنری برای فیلدها
#     field_dict = {
#         'id': models.AutoField(primary_key=True),  # فیلد کلید اصلی
#     }

#     # اضافه کردن فیلدهای داینامیک
#     for field in fields:
#         field_type = getattr(models, field.type, models.CharField)  # گرفتن نوع فیلد از Django Models
#         field_dict[field.name] = field_type(max_length=255)  # تنظیم طول برای فیلدهای متنی

#     # ساخت کلاس مدل داینامیک
#     DynamicModel = type(table_name, (models.Model,), {
#         '__module__': __name__,  
#         'Meta': type('Meta', (), {'app_label': 'persons'}),  
#         **field_dict
#     })

#     # ثبت مدل جدید در اپلیکیشن
#     apps.all_models['persons'][table_name.lower()] = DynamicModel
#     # 🚀 راه‌حل: غیرفعال کردن `FOREIGN KEY` قبل از اجرای `schema_editor`
#     with connection.cursor() as cursor:
#         cursor.execute("PRAGMA foreign_keys=OFF;")  # 🔴 غیرفعال کردن
#         try:
#             with connection.schema_editor() as schema_editor:
#                 schema_editor.create_model(DynamicModel)
#         finally:
#             cursor.execute("PRAGMA foreign_keys=ON;")  # ✅ دوباره فعال‌سازی
#     # with connection.cursor() as cursor:
#     #     cursor.execute("PRAGMA foreign_keys = OFF;")  # خاموش کردن قیود کلید خارجی

#     # with connection.schema_editor() as schema_editor:
#     #     schema_editor.create_model(DynamicModel)

#     # with connection.cursor() as cursor:
#     #     cursor.execute("PRAGMA foreign_keys = ON;")  # دوباره فعال کردن قیود کلید خارجی
