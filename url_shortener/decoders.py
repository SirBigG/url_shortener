import string
from math import floor


class Base62:
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase

    @classmethod
    def encode(cls, num: int, b: int = 62) -> str:
        if b <= 0 or b > 62:
            return "0"
        r = num % b
        res = cls.base[r]
        q = floor(num / b)
        while q:
            r = q % b
            q = floor(q / b)
            res = cls.base[int(r)] + res
        return res

    @classmethod
    def decode(cls, num: str, b: int = 62) -> int:
        limit = len(num)
        res = 0
        for i in range(limit):
            res = b * res + cls.base.find(num[i])
        return res
