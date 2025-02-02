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