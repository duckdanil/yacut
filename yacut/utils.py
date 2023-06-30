import random
import string

from settings import LENGTH_SHORT_ID
from yacut.models import URLMap


def get_short(short):
    if short and short != '':
        return short
    symbols = string.ascii_letters + string.digits
    while True:
        new_short = ''.join((random.choice(symbols) for _ in range(LENGTH_SHORT_ID)))
        if URLMap.query.filter_by(short=new_short).first() is None:
            return new_short
