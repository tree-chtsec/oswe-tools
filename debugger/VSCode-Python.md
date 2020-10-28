# VSCode + Python Extension

1. 要被 debug 的程式得先在 code 最前面加入以下幾行, 然後直接跑起來!

```python
# 記得先 pip install ptvsd
import ptvsd
ptvsd.enable_attach(redirect_output=True)
ptvsd.wait_for_attach()
```

2. 本地要有一份相同的 code / 資料夾結構, 可以用 rsync

3. 在 VSCode 安裝 Python Extension. 

4. 把整個資料夾拖進 VSCode, 選定 Main function 後 ( 如 app.py ), ctrl+shift+D > 新增 launch.json
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "port": <remote-port>,
            "host": "<remote-host>",
            "pathMappings": [{
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "/path/to/code/"
            }],
        }
    ]
}
```

5. 跑起來!
