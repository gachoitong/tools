# import pickle
import re
import json
# import numpy as np
# import pandas as pd
from pathlib import Path
# from bxv.funcs import load_pickle, dump_pickle, jsonRead, jsonSave


def jsonRead(filepath, encoding='utf8'):
    with open(filepath, 'r', encoding=encoding) as f:
        ndata = json.load(f)
    return ndata


_cur_dir = Path(__file__).parent.resolve()


def _extract_zh_chars(ss):
    arr = []
    pj = 0
    for m in re.finditer('[\u4E00-\u9FFF]+',  ss):
        i, j = m.span()
        if i > 0:
            arr.append((False, ss[pj:i]))
        arr.append((True, ss[i:j]))
        pj = j
    if pj < len(ss):
        arr.append((False, ss[pj:]))
    return arr


# load dict

# _dict_files = ['dict_toen', 'dict_tohv',
#                'dict_topyf', 'dict_tovp', 'dict_tosp', 'dict_tojy']


_dict_files = ['dict_tohv', 'dict_topyf', 'dict_tovp']

# _dict_files_pickle = [
#     Path(_cur_dir, 'data', f'{i}.pickle') for i in _dict_files]

_dict_files_json = [Path(_cur_dir, 'data', f'{i}.json') for i in _dict_files]


# dict_toen, dict_tohv, dict_topy, dict_tovp, dict_tosp, dict_tojy = [ load_pickle(f) for f in _dict_files_pickle]

dict_tohv, dict_topy, dict_tovp, = [
    jsonRead(f) for f in _dict_files_json]

print(__name__, 'loaded {} dictionaries'.format(len(_dict_files_json)))


def dict_get_value(dict, key, default=None, clean_func=None):
    if key in dict:
        return clean_func(dict[key]) if clean_func else dict[key]
    else:
        return default


def translate_sentence(sentence, trans_hz_func, sep=' '):
    return sep.join(list(map(trans_hz_func, list(sentence))))


# vp

def _clean_func_vp(ss):
    return ss.split('/')[0]


def hz2vp(w, df=""):
    """
    single word to vietphase
    """
    return dict_get_value(dict_tovp, w, df, clean_func=_clean_func_vp)


# hv

def _clean_func_hv(x):
    return x.split(',')[0]


def hz_to_hv_raw(w, df=""):
    """
    single word to hanviet raw content
    """
    return dict_get_value(dict_tohv, w, df)


def hz_to_hv(w, df=""):
    """
    single word to hanviet
    """
    return dict_get_value(dict_tohv, w, df, clean_func=_clean_func_hv)


def hzs_to_hv(w):
    """
    sentence to hanviet
    """
    return translate_sentence(w, hz_to_hv)


_py_tonemarks = ["", "̄", "́", "̌", "̀", ""]

_py_normalize = (('\u0061\u0304', '\u0101'),
                 ('\u0061\u0301', '\u00E1'),
                 ('\u0061\u030C', '\u01CE'),
                 ('\u0061\u0300', '\u00E0'),
                 ('\u0065\u0304', '\u0113'),
                 ('\u0065\u0301', '\u00E9'),
                 ('\u0065\u030C', '\u011B'),
                 ('\u0065\u0300', '\u00E8'),
                 ('\u006F\u0304', '\u014D'),
                 ('\u006F\u0301', '\u00F3'),
                 ('\u006F\u030C', '\u01D2'),
                 ('\u006F\u0300', '\u00F2'),
                 ('\u0069\u0304', '\u012B'),
                 ('\u0069\u0301', '\u00ED'),
                 ('\u0069\u030C', '\u01D0'),
                 ('\u0069\u0300', '\u00EC'),
                 ('\u0075\u0304', '\u016B'),
                 ('\u0075\u0301', '\u00FA'),
                 ('\u0075\u030C', '\u01D4'),
                 ('\u0075\u0300', '\u00F9'),
                 ('\u0076\u0304', '\u0076'),
                 ('\u0076\u0301', '\u0076'),
                 ('\u0076\u030C', '\u0076'),
                 ('\u0076\u0300', '\u0076'),)


def normalize_py_tone(s):
    if not s:
        return s
    for i, j in _py_normalize:
        s = s.replace(i, j)
    return s


def remove_py_tone(s):
    if not s:
        return s
    for i, j in _py_normalize:
        s = s.replace(j, i)
    for i in _py_tonemarks:
        s = s.replace(i, '')
    return s


def _clean_func_py(s, add_tone=True):
    if not s:
        return s
    s = s[0]
    pinyin = s[:-1]
    if not add_tone:
        return pinyin
    tone = int(s[-1])
    # Find first vowel -- where we should put the diacritical mark
    vowels = (c for c in pinyin if c in "aeoiuv")
    vowel = pinyin.index(next(vowels)) + 1
    pinyin = pinyin[:vowel] + _py_tonemarks[tone] + pinyin[vowel:]
    return normalize_py_tone(pinyin)


def _clean_func_py_without_tone(s):
    return _clean_func_py(s, add_tone=False)


def hz_to_py(w, df=""):
    """
    single word to pinyin
    """
    return dict_get_value(dict_topy, w, df, clean_func=_clean_func_py)


def hzs_to_py(s):
    """
    translate full sentence to pinpyin
    """
    return translate_sentence(s, hz_to_py)


def hz_to_py_no_tone(w, df=""):
    """
    single word to pinyin
    """
    return dict_get_value(dict_topy, w, df, clean_func=_clean_func_py_without_tone)


def hzs_to_py_no_tone(s):
    """
    translate full sentence to pinpyin
    """
    return translate_sentence(s, hz_to_py_no_tone)


def lookup(s, dict, clean_func=None):
    n = len(s)
    if n == 0:
        return []
    i = n
    while i > 0:
        key = s[:i]
        if key in dict:
            value = dict[key]
            if value is None:
                value = ''
            if clean_func is not None:
                value = clean_func(value)
            rs = [(key, value), ]
            if i < n:
                rs.extend(lookup(s[i:], dict, clean_func))
            return rs
        else:
            i += -1
    # if all key not in dict
    # return (key,none) increase 1
    a = [(s[:1], None)]
    if n > 1:
        a.extend(lookup(s[1:], dict, clean_func))
    return a


# lookup('我明白a你说', dict_tovp)
# [('我明白', 'ta hiểu rồi'), ('a', None), ('你', 'ngươi/cậu'), ('说', 'nói')]

def lookup_join_value(s, dict, clean_func=None, sep=" "):
    a = lookup(s, dict, clean_func)
    return sep.join([j for _, j in a if j is not None])


def array_split_by_value(arr, value_func=None):
    x = []
    if value_func is None:
        def value_func(x): return x
    item = arr[0]
    mask = value_func(item)
    x.append((mask, [item, ]))
    for item in arr[1:]:
        nmask = value_func(item)
        if mask == nmask:
            x[-1][1].append(item)
        else:
            mask = nmask
            x.append((mask, [item, ]))
    return x


def transpose(a):
    return list(zip(*a))


# transpose(((1, 2), (3, 4)))


def _translate_phrase(s, jy=False):
    jy = False
    # for _ in trange(100000):
    a = lookup(s, dict_tovp, lambda x: x.split('/')[0])
    b = []
    for i, j in a:
        hv = lookup_join_value(i, dict_tohv, clean_func=_clean_func_hv)
        if jy:
            # py = lookup_join_value(i, dict_tojy, clean_func=_clean_func_jy)
            pass
        else:
            py = lookup_join_value(i, dict_topy, clean_func=_clean_func_py)

        if j is None:
            j = hv
        b.append((i, py, hv, j))
    c = []
    # join all nearby null phrases to 1
    for i, j in array_split_by_value(b, lambda i: i[1] == i[2] == i[3] == ''):
        if not i:
            c.extend(j)
        else:
            c.append((''.join([k[0] for k in j]), '', '', ''))
    return c


_punc_replacments = [('！', '!'),
                     ('？', '?'),
                     ('｡', '.'),
                     ('。', '.'),
                     ('＂', '"'),
                     ('＃', '#'),
                     ('＄', '$'),
                     ('％', '%'),
                     ('＆', '&'),
                     ('＇', '\''),
                     ('（', '('),
                     ('）', ')'),
                     ('＊', '*'),
                     ('＋', '+'),
                     ('，', ','),
                     ('－', '-'),
                     ('／', '/'),
                     ('：', ':'),
                     ('；', ';'),
                     ('＜', '<'),
                     ('＝', '='),
                     ('＞', '>'),
                     ('＠', '@'),
                     ('［', '['),
                     ('＼', '\\'),
                     ('］', ']'),
                     ('＾', '^'),
                     ('＿', '_'),
                     ('｀', '`'),
                     ('｛', '{'),
                     ('｜', '|'),
                     ('｝', ']'),
                     ('～', '~'),
                     ('｟', '('),
                     ('｠', '_'),
                     ('｢', '['),
                     ('｣', ']'),
                     ('､', ','),
                     ('、', ','),
                     ('〃', '"'),
                     ('》', '>'),
                     ('「', '['),
                     ('」', ']'),
                     ('『', '['),
                     ('』', ']'),
                     ('【', '['),
                     ('】', ']'),
                     ('〔', '['),
                     ('〕', ']'),
                     ('〖', '['),
                     ('〗', ']'),
                     ('〘', '['),
                     ('〙', ']'),
                     ('〚', '['),
                     ('〛', ']'),
                     ('〜', '~'),
                     ('〝', '"'),
                     ('〞', '"'),
                     ('〟', ','),
                     ('〰', '~'),
                     ('〾', ','),
                     ('〿', ','),
                     ('–', '-'),
                     ('—', '-'),
                     ('‘', '\''),
                     ('’', '\''),
                     ('‛', '\''),
                     ('“', '"'),
                     ('”', '"'),
                     ('„', ','),
                     ('‟', '"'),
                     ('…', '...'),
                     ('‧', '.'),
                     ('﹏', '~'),
                     ('.', '.')]


def _replace_punc(s):
    for i, j in _punc_replacments:
        s = s.replace(i, j)
    return s


def _text_clean(s, normal_punc=True):
    if not s:
        return s
    s = s.replace('  ', ' ')
    if normal_punc:
        s = _replace_punc(s)
    return s.replace('  ', ' ').strip().replace(' .', '.').replace(' ,', ',').replace(' :', ':')


def translate(s='明白', cols=None, jy=False, adv=False):
    """
    default:
    translate('我明白你说')

    [['我明白', 'wǒ míng bái', 'ngã minh bạch', 'ta hiểu rồi'],
    ['你', 'nǐ', 'nễ', 'ngươi'],
    ['说', 'shūo', 'duyệt', 'nói']]

    custom cols:
    translate('我明白你说',cols=['py','zh','vi'])

    [['wǒ míng bái', '我明白', 'ta hiểu rồi'],
    ['nǐ', '你', 'ngươi'],
    ['shūo', '说', 'nói']]

    advance:
    translate('我明白你说',adv=True)

    ('我明白你说',
    'wǒ míng bái nǐ shūo',
    'ta hiểu rồi ngươi nói',
    'ngã minh bạch nễ duyệt',
    '我明白 tahiểurồi 你 ngươi 说 nói',
    [['我明白', 'wǒ míng bái', 'ngã minh bạch', 'ta hiểu rồi'],
      ['你', 'nǐ', 'nễ', 'ngươi'],
      ['说', 'shūo', 'duyệt', 'nói']])

    """
    if not s:
        return []
    a = _extract_zh_chars(s)
    x = []
    for is_zh, zh_str in a:
        if is_zh:
            x.extend(_translate_phrase(zh_str, jy=jy))
        else:
            x.append((zh_str, '', '', ''))

    rs = [[j.strip() for k, j in enumerate(i)] for i in x]
    if adv:
        vi = _text_clean(
            ' '.join([i[3] if (i[3] or i[1]) else i[0] for i in rs]))
        py = _text_clean(' '.join([i[1] if i[1] else i[0] for i in rs]))
        hv = _text_clean(' '.join([i[2] if i[2] else i[0] for i in rs]))
        zhvi = _text_clean(' '.join('{} {}'.format(
            j[0], j[3].replace(' ', '')) for j in rs))
      
    if cols:
        colis = {'hz': 0, 'zh': 0,  'py': 1, 'hv': 2, 'vp': 3, 'vi': 3}
        rs = [[i[colis[c]] for c in cols] for i in rs]

    if adv:
        return s.strip(), py, vi, hv, zhvi, rs
    return rs
