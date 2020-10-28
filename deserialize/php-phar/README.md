# php unserialize without unserialize

## Thanks to `phar://`, we can trigger unserialize whenever file system call.

## Affected Method
| | | |
|-|-|-|
| fileatime | filectime   | file\_exists | file\_get\_contents | file\_put\_contents | is\_writeable |
| file      | filegroup   | fopen       | fileinode         | filemtime         | readfile     |
| fileowner | fileperms   | is\_dir      | is\_executable     | is\_file           | stat         |
| is\_link   | is\_readible | is\_writable | parse\_ini\_file    | copy              | unlink       |

## Quick Start
```bash
$ php phar_generate.php
$ php phar_vuln.php
```

## Reference

* https://medium.com/@knownsec404team/extend-the-attack-surface-of-php-deserialization-vulnerability-via-phar-d6455c6a1066
