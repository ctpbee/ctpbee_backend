from random import choice
from string import ascii_letters as s, digits as d

gen_key = lambda: ''.join([choice(s + d) for _ in range(32)])

BAR_TIME = 3
# key
SECRET_KEY = gen_key()
JWT_SECRET_KEY = gen_key()


