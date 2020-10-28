# Python Debugger (PDB)
```bash
$ python -m pdb XXX.py
```

```python
# 列出當前原始碼的位置
(Pdb) l[ist]

# 設定中斷點 by 函式
(Pdb) break <function-name>

# 設定中斷點 by 行數
(Pdb) break <line No,>

# 繼續執行到中斷點
(Pdb) c[ont]

# 執行一行 ( 會跳進 function )
(Pdb) s[tep]

# 在當前 Context 跑 Python Code
(Pdb) !print('hello')

# 列出當前堆疊
(Pdb) bt

# 往上跳一層 function ( ex. A() 呼叫 B(), 當前在B, 則可以跳到 A )
(Pdb) up

# 往下跳一層 function
(Pdb) down

# 不知道要輸入什麼指令時
(Pdb) ?

# 不知道那個指令有什麼作用時
(Pdb) help XXX

# 退出
(Pdb) q[uit]

```
