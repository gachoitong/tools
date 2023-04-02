# zhtools
requires: PyQt5,clipboard

```
pip install PyQt5
pip install clipboard
```


use as gui app: app_translate.bat

![Screenshot (13720)](https://user-images.githubusercontent.com/129648042/229337233-4d09eb35-3fd4-43de-9fda-a86262dbd2e8.png)


import to your project

```


from app_translate_lib.py import translate


# default:
translate('我明白你说')

# return

[['我明白', 'wǒ míng bái', 'ngã minh bạch', 'ta hiểu rồi'],
['你', 'nǐ', 'nễ', 'ngươi'],
['说', 'shūo', 'duyệt', 'nói']]

# custom cols:
translate('我明白你说',cols=['py','zh','vi'])

# return

[['wǒ míng bái', '我明白', 'ta hiểu rồi'],
['nǐ', '你', 'ngươi'],
['shūo', '说', 'nói']]

# advance:
translate('我明白你说',adv=True)

# return

('我明白你说',
'wǒ míng bái nǐ shūo',
'ta hiểu rồi ngươi nói',
'ngã minh bạch nễ duyệt',
'我明白 tahiểurồi 你 ngươi 说 nói',
[['我明白', 'wǒ míng bái', 'ngã minh bạch', 'ta hiểu rồi'],
    ['你', 'nǐ', 'nễ', 'ngươi'],
    ['说', 'shūo', 'duyệt', 'nói']])
```
