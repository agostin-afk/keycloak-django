import random
chars = 'abcdefghijklmnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVXYZ' \
        '0123456789' \
        '#()^[]-_*%&=+/'

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])
print(SECRET_KEY)