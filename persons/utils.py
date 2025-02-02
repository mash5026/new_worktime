import re


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
