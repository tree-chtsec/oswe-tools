
## Java Debugger (JDB) 遠端除錯
> 需要以 `java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=8000 -jar xxx.jar`  執行
```bash
$ jdb -attach <remote-host>:<remote-port>
```

```jdb

# 執行一行 ( 會跳進 function )
> step
> stepi

# 執行到當前 function 結尾
> step up

# 設中斷點，這邊要寫 class 全名
> stop in a.b.c.ClassName.MethodName

# 如果遇到相同 function 有多個參數(多載)，型態要記得寫全名
> stop in com.offsec.awae.answers.dao.QuestionDao.insertQuestion(java.lang.String, java.lang.String, int, int, boolean, boolean)
# 否則...
Unable to set breakpoint com.offsec.awae.answers.dao.QuestionDao.insertQuestion : Method insertQuestion is overloaded; specify arguments

# 列出當前原始碼的位置 ( 需要指定 --sourcepath /path/to/source 才行 )
> list

# 區域變數
> locals

# 清除單一中斷點
> clear a.b.c.ClassName.MethodName

# 在當前 Context 跑 Java Code
> eval java.lang.System.currentTimeMillis();
```

