# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 14:27
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: sort_magnet_result.py
# @Software: PyCharm

from app.const import *


def sort_magnet_result(magnet_result: list, sort_key: int, is_reverse: bool = True):
    if sort_key == SORTED_BY_DEFAULT:
        pass
    else:
        if sort_key == SORTED_BY_DATE:
            sort_key_as_str = 'format_create_date'
            key_func = lambda k: k.get(sort_key_as_str, '0')
        elif sort_key == SORTED_BY_SIZE:
            sort_key_as_str = 'size_as_mb'
            key_func = lambda k: k.get(sort_key_as_str, 0)
        elif sort_key == SORTED_BY_POPULAR:
            sort_key_as_str = 'popular'
            key_func = lambda k: float(k.get(sort_key_as_str) or 0)
        magnet_result.sort(key=key_func, reverse=is_reverse)
