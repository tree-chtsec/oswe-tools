# VSCode + NodeJS

1. 需要以 `node --inspect=0.0.0.0:9229 /path/to/bin/www` 執行

2. 本地要有一份相同的 code / 資料夾結構, 可以用 rsync

3. 把整個資料夾拖進 VSCode, ctrl+shift+D > 新增 launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "attach",
            "name": "Launch Program",
            "skipFiles": [
                "<node_internals>/**"
            ],
            "port": 9229,
            "address": "<ip>",
            "localRoot": "${workspaceRoot}",
            "remoteRoot": "/path/to/code/"
        }
    ]
}
```

4. 跑起來!
